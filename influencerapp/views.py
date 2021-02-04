from django.shortcuts import render

# Create your views here.
from django.shortcuts import render,redirect
from rest_framework.response import Response
# Create your views here.
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from influencerapp.forms import *

import requests,json
from django.shortcuts import render,redirect
from django.http import HttpResponse,HttpResponseRedirect,StreamingHttpResponse
import binascii
import os
from django.core.files.storage import FileSystemStorage

from .config import Config as cfg
import shopify
import requests
from datetime import datetime

from .models import Shop_data
from django.views.decorators.csrf import csrf_exempt
import pandas as pd
from django.conf import settings
# shop=None
# token=None
shop1=None

# Create your models here.
@csrf_exempt   
def home1(request):
    return render(request, 'welcome.html')


@csrf_exempt
def home(request):
    return render(request, 'index2.html')


# shopify.Session.setup(api_key=API_KEY, secret=API_SECRET)
# In order to access a shop's data, apps need an access token from that specific shop. We need to authenticate with that shop using OAuth, which we can start in the following way:

# shop_url = "SHOP_NAME.myshopify.com"
# api_version = '2020-10'
# state = binascii.b2a_hex(os.urandom(15)).decode("utf-8")
# redirect_uri = "http://myapp.com/auth/shopify/callback"
# scopes = ['read_products', 'read_orders']

# newSession = shopify.Session(shop_url, api_version)
# auth_url = newSession.create_permission_url(scopes, redirect_uri, state)
# # redirect to auth_url
@csrf_exempt   
def install(request):
    shop = request.GET.get('shop')
    code = request.GET.get('hmac')
    print("shop : ",shop)
    print("hmac : ",code)
    global Shop1
    shop1=shop
    api_version = '2020-10'
    state = binascii.b2a_hex(os.urandom(15)).decode("utf-8")
    shopify.Session.setup(api_key=cfg.SHOPIFY_CONFIG["API_KEY"], secret=cfg.SHOPIFY_CONFIG["API_SECRET"])
    newSession = shopify.Session(shop, api_version)
    scope = ["read_products","read_orders"]
    print(cfg.SHOPIFY_CONFIG["REDIRECT_URI"])
    permission_url = newSession.create_permission_url(scope,cfg.SHOPIFY_CONFIG["REDIRECT_URI"],state)
    print("permission_url : ",permission_url)
    return HttpResponseRedirect(permission_url)


@csrf_exempt
def connect(request):
    # global shop,token
    shop = request.GET.get("shop")
    request.session['token'] = str(shop)
    code = request.GET.get('code')
    timestamp = request.GET.get("timestamp")
    hmac = request.GET.get("hmac")
    global Shop1
    
    shop1=shop
    params = {
        "client_id": cfg.SHOPIFY_CONFIG["API_KEY"],
        "client_secret": cfg.SHOPIFY_CONFIG["API_SECRET"],
        "code": code,
    }

    print("params : ",params)
    response = requests.post("https://"+str(shop)+"/admin/oauth/access_token", data=params)
    # request.session['shop'] = str(shop)
    token = json.loads(response.text)['access_token']
    request.session['token'] = str(token)
    print('tokentokentokentokentokentokentokentokentokentokentoken',token)
    data=Shop_data.objects.filter(shop=shop).exists()
    print("datadatadatadata",data)
    json1={
    "webhook": {
    "topic": "app/uninstalled",
    "address": "https://"+str(request.get_host()) + "/uninsta",
    "format": "json"
    }
    }
    print(json1)
    headers={"x-shopify-access-token":token,"content-type":"application/json","cache-control":"no-cache"}
    if data==False:
        print("database ma ni ha")
        shop_data = Shop_data(shop=shop,api_key=cfg.SHOPIFY_CONFIG["API_KEY"],token=token,status=True,)
        shop_data.save()
        p3=requests.post("https://influencersclubs.myshopify.com/admin/api/2021-01/webhooks.json",headers=headers,json=json1)
        print(p3.json())
        print("webhook created sucessfully")
    session = shopify.Session(shop, '2020-10', token)
    shopify.ShopifyResource.activate_session(session)

    return HttpResponseRedirect('/home?shop='+shop+'/')

@csrf_exempt   
def launch(request):
    # global shop,token
    url=request.get_host()+'/uninstall/'
    try:
        dang=request.GET["user"]
        print(dang)
    except:
        return redirect('/signin/')
    print("url",url)
    user=request.user
    print("userrrrrrrrrrrrrrrrrrrrrrr",user)
    return render(request, 'launch.html',{"user":user})

    
# @login_required
@csrf_exempt   
def dash(request):
    # global shop,token
    try:
        name=request.GET["user"]
        print(name)
    except:
        return redirect('/signin/')
    try:
        shop=request.GET["shop"]
        print(shop)
    except:
        return redirect('/signin/')
    print("jai mata di", shop)
    shop=str(shop).replace("/","")
    de= Shop_data.objects.filter(shop=shop)
    token=""
    api_keys=""
    for i in de:
        token=i.token
        api_keys=i.api_key
    print(shop,token)
    p=requests.get("https://"+shop+"/admin/api/2021-01/orders/count.json?status=any",auth=(api_keys,token))
    count = json.loads(p.text)# s.split("delimiter")
    count=count["count"]
    print("countcount",count)
    p=requests.get("https://"+shop+"/admin/api/2021-01/orders.json?status=any",auth=(api_keys,token))
    orders = json.loads(p.text)# s.split("delimiter")
    print("-------------------------------------------")
    print(orders)
    print("-------------------------------------------")
    orders_data=[]
    for i in orders["orders"]:
        email=i["email"]
        print("emailemailemailemailemail",email)
        shopify_data={"email":email,"shopify_data":i}
        print("shopify_data")
        headers={"Authorization":"Token 4d5a47c94bca77271073dd128f62d0c75e722b24"}
        p3=requests.post("https://api.influencers.club/api/filter/email",headers=headers,json=shopify_data)
        data=p3.json()
        chko=""
        try:
            chko=data["meesage"]
        except:
            pass
        if chko=="No data available":
            continue
        if data not in orders_data:
            orders_data.append(data)
    print(orders_data)
    dis=len(orders_data)
    return render(request, 'dashboard.html',{'data':orders_data,'dis':dis})

    # if request.method=='POST' and 'csv' in request.POST:
    #     print("yessssssssssssssssss")
    #     excel_file = request.FILES["csvs"]
    #     file=str(excel_file)
    #     print("excel_fileexcel_fileexcel_fileexcel_file",excel_file)
    #     if file[-1]=="s" and file[-2]=="l" and file[-3]=="x":
    #         df=pd.read_excel(excel_file)
    #     if file[-1]=="v" and file[-2]=="s" and file[-3]=="c":
    #         df=pd.read_csv(excel_file,encoding='utf-8')
    #     if file[-1]=="x" and file[-2]=="s" and file[-3]=="l" and file[-4]=="x":
    #         df=pd.read_excel(excel_file)
    #     return HttpResponse(df.to_html())

    # return render(request, 'dash1.html')

from rest_framework.views import APIView
#jai mata di
# from .serializers import *
class Current_PairAPIView(APIView):
    def post(self, request, format=None):
    # shop = request.GET.get("shop")
        data= request.data
        print("DONE",data['myshopify_domain'])
        shop=data['myshopify_domain']
        de= Shop_data.objects.filter(shop=shop).delete()
        return Response(status=200)

# def uninstall(request):
#     if request.method=="POST":
#     # global shop,token
#         shop = request.GET.get("shop")
#         # shop="influencersclubs.myshopify.com"
#         print("shopshopshopshopshopshop",shop)
#         de= Shop_data.objects.filter(shop=shop).delete()
#         return Response(status=200)
    # print(de[0].token)
    

    # return Response("done")



@csrf_exempt   
def signup_page(request):
    try:
        shop=request.GET["shop"]
        print(shop)
    except:
        return redirect('/signin/?shop='+shop+'/')
    if request.method=="POST":
        form=signupform(request.POST)
        if form.is_valid():
            name=request.POST["Name"]
            email=request.POST["Email"]
            password=request.POST["Password"]
            Firstname=request.POST["Firstname"]
            lastname=request.POST["lastname"]
            user = User.objects.create_user(username=name,email=email,password=password,first_name=Firstname,last_name=lastname)
            user.save()
            return redirect('/signin/?shop='+shop+'/')
    else:
        form = signupform()
        print("notdshksfdhjsdfhsdfahlsafd")
    return render(request,'signup.html',{"form":form})





@csrf_exempt   
def login_user(request):
    try:
        shop=request.GET["shop"]
        print(shop)
    except:
        pass
    if request.user.is_authenticated:
        print("Logged in")
        print(request.user,"request.user")
        username=request.user
        try:
            user = authenticate(username=username, password=password)
            if user:
                print("yesssssssssssssssss")
                login(request,user)

        except:
            pass
        return redirect("/launch?user="+str(username)+'&shop='+shop)
    else:
        print("Not logged in")

    if request.method == 'POST':
        form = loginform(request.POST)
        if form.is_valid():
            username = request.POST.get('Username')
            print(username)
            password = request.POST.get('Password')
            print(password)
            user = authenticate(username=username, password=password)
            if user:
                print("yesssssssssssssssss")
                login(request,user)
                # print("sessssssssssssssssssssssssss",request.session['user'])
                return redirect("/launch?user="+username+'&shop='+shop)

    else:
        form = loginform()
        print("not")
    return render(request, 'signin.html', {"form": form})



@csrf_exempt   
def user_logout(request):
    logout(request)
    try:
        shop=request.GET["shop"]
        print(shop)
    except:
        return redirect('/signin/')
    return redirect('/signin?shop='+shop+'/')


@csrf_exempt   
def upload_csv(request):
    try:
        status=request.GET["status"]
        user=request.GET["user"]
        de= User.objects.filter(username=user)
        email=""
        for i in de:
            email=i.email
        print(email,"emailemailemailemailemailemail")
        if str(status)=="status":
            headers={"Authorization":"Token 4d5a47c94bca77271073dd128f62d0c75e722b24"}
            p3=requests.get("https://api.influencers.club/api/filter/csv/retrieve/"+str(email),headers=headers)
            print(p3)
            data=p3.json()
            print(data)
            return render(request, 'uploadcsv.html',{"data":data})
    except:
        pass
  

    if request.method=='POST' and 'csv' in request.POST:
        print("yessssssssssssssssss")
        excel_file = request.FILES["csvs"]
        namefile=str(excel_file)
        fs = FileSystemStorage()
        filename = fs.save(namefile, excel_file)

        # print(excel_file)
        # print(type(excel_file))
        # file=str(excel_file)
        # print("excel_fileexcel_fileexcel_fileexcel_file",excel_file)
        # if file[-1]=="s" and file[-2]=="l" and file[-3]=="x":
        #     df=pd.read_excel(excel_file)
        # if file[-1]=="v" and file[-2]=="s" and file[-3]=="c":
        #     df=pd.read_csv(excel_file,encoding='utf-8')
        # if file[-1]=="x" and file[-2]=="s" and file[-3]=="l" and file[-4]=="x":
        #     df=pd.read_excel(excel_file)
        # path="D:/D drive Amit/amit/Ajupyter/"

        # text = open(os.path.join(settings.MEDIA_ROOT, 'a.txt'), 'rb').read()
        fil=open(os.path.join(settings.MEDIA_ROOT,str(namefile)),'rb')
        print("pathhhhhhhhhhhhhhhhhhhh",os.path.join(settings.MEDIA_ROOT))
        files = {'input_file':fil }
        user=request.GET["user"]
        de= User.objects.filter(username=user)
        email=""
        for i in de:
            email=i.email
        params = {
                "email": email,
            }

        headers={"Authorization":"Token 4d5a47c94bca77271073dd128f62d0c75e722b24"}

        p3=requests.post("https://api.influencers.club/api/filter/csv/create/",headers=headers,data=params,files=files)
        data=p3.json()
        print(data)
        fil.close()
        os.remove(str(os.path.join(settings.MEDIA_ROOT))+"/"+str(namefile))
       
        return render(request, 'uploadcsv.html',{"data":data})
        return HttpResponse(df.to_html())

    return render(request, 'uploadcsv.html')