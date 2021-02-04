from django.contrib import admin

# Register your models here.
from influencerapp.models import *

class AdAdmin(admin.ModelAdmin):
    list_display = ['shop_id', 'shop', 'api_key', 'token','status','created_at','updated_at' ]

admin.site.register(Shop_data,AdAdmin)


 # shop_id = models.AutoField(primary_key=True)
 #    shop = models.CharField(max_length=500,editable=True)
 #    api_key = models.CharField(max_length=100,editable=True)
 #    token = models.CharField(max_length=100,editable=True)
 #    status = models.BooleanField(default=False)
 #    created_at = models.DateTimeField(auto_now_add=True,editable=True,)
 #    updated_at = models.DateTimeField(auto_now=True,editable=True,)
