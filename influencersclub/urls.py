"""influencersclub URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from influencerapp import views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.home1, name="home1"),
    path('connect/',views.connect, name="connect"),
    path('install/',views.install, name="install"),
    path('launch/',views.launch, name="index"),
    path('dash/',views.dash, name="dash"),
    path('home/',views.home, name="home"),
    # path('uninsta',views.Current_PairAPIView.as_view(), name ="uninstall"),
    path('uninsta',views.Current_PairAPIView.as_view(), name ="getuninsta"),
    # path('uninstall/',views.uninstall, name="uninstall"),
    path('signup/',views.signup_page, name='signup'),
    path('signin/',views.login_user, name='signin'),
    path('logout/',views.user_logout, name='user_logout'),
    path('upload_csv/',views.upload_csv, name='upload_csv'),
    
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)