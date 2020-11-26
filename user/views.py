from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from .models import UserProfile
from django.contrib.auth.models import User
from django.urls import reverse
import random

@csrf_exempt
def dashboard(request):
    if request.user.id:
        print("Logging In")
        userprofile=UserProfile.objects.get(id=request.user.id)
        u = User.objects.all()
        q=UserProfile.objects.all()
        obj={'userprofile':userprofile,'u':u,'q':q,'UserProfile':UserProfile.objects.all()}
        return render(request, "user/dashboard.html",obj)
    else:
        print('logging out')
        return render(request, "user/dashboard.html")
    
    
    
@csrf_exempt
def content(request,id):
    user=UserProfile.objects.get(id=id)
    u = User.objects.all()
    q=UserProfile.objects.all()
    obj={'user':user,'u':u,'q':q,'UserProfile':UserProfile.objects.all()}
    return render(request,'user/content.html',obj)

@csrf_exempt
def allocateChild(request,id):
    child_id=random.randrange(95,176,)
    if is_freeChild(child_id,id):
        child=UserProfile.objects.get(id=child_id)
        child.parent_id=id
        child.save()
        parent=UserProfile.objects.get(id=id)
        parent.child_id=child_id
        parent.is_child_assigned=True
        parent.save()
    else:
        allocateChild(request,id)
    
    return HttpResponseRedirect(reverse('dashboard' ))

def is_freeChild(child_id,id):
    parent=UserProfile.objects.get(id=child_id)#for assuring that we are not assigning mom as child
    if child_id==id and child.child_id==id:
        return False
    child=UserProfile.objects.get(id=child_id)
    if child.parent_id:
        return False
    return True
