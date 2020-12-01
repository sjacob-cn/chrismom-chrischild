"""cmcs URL Configuration

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
from django.conf.urls import url,include
from django.urls import path,include
from user.views import dashboard,content,allocateChild,chat,reply,comment,passwordreset,viewTasks

urlpatterns = [
    path('admin/', admin.site.urls),
    path('user/', include("user.urls")),
    path("", dashboard, name="dashboard"),
    path("accounts/", include("django.contrib.auth.urls")),
    path('<int:id>/content/',content,name='content'),
    path('<int:id>/allocateChild/',allocateChild,name='allocateChild'),
    path('chat/',chat,name='chat'),
    path('<int:id>/chat/',reply,name='reply'),
    path('chat.../',comment,name='comment'),
    path('display/',viewTasks,name='tasks'),
    
    path('accounts/reset-password/', passwordreset, name='contact')
    
    

   
    
    
    
]
