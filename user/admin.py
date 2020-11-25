# from django.conf.urls import include, url
from django.contrib import admin
from . models import UserProfile,Comment, Reply

admin.site.register(UserProfile)
admin.site.register(Comment)
admin.site.register(Reply)