from django.db import models
import datetime
from django.conf import settings

# Create your models here.

class UserProfile(models.Model):
    user = models.ForeignKey( settings.AUTH_USER_MODEL, null = False, on_delete=models.CASCADE)
    child = models.ForeignKey(settings.AUTH_USER_MODEL, null = True, related_name = "+" ,on_delete=models.CASCADE)
    parent = models.ForeignKey(settings.AUTH_USER_MODEL, null = True,related_name = "+", on_delete=models.CASCADE)
    picture = models.TextField()
    team_name = models.CharField(max_length=100)
    is_password_reset = models.BooleanField(default = False)
    is_child_assigned = models.BooleanField(default = False)
    created_at = models.DateTimeField(auto_now_add=True) 
    updated_at = models.DateTimeField(auto_now=True)
    

    def __str__(self):
        return str(self.user)

class Comment(models.Model):
    
    user = models.ForeignKey( settings.AUTH_USER_MODEL, null = False, on_delete=models.CASCADE)
    comment=models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    receiver=models.IntegerField(null=True)
    def __str__(self):
        return str(self.user)

class Reply(models.Model):
    user = models.ForeignKey( settings.AUTH_USER_MODEL, null = False, on_delete=models.CASCADE)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE )
    comments=models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return str(self.user)