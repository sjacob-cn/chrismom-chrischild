from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from .models import UserProfile
from django.contrib.auth.models import User
from django.urls import reverse

import random
@csrf_exempt
def dashboard(request):
    return render(request, "user/dashboard.html")

def content(request,id):
    user=UserProfile.objects.get(id=id)
    u = User.objects.all()
    q=UserProfile.objects.all()
    obj={'user':user,'u':u,'q':q,'UserProfile':UserProfile.objects.all()}
    return render(request,'user/content.html',obj)

@csrf_exempt
def allocateChild(request,id):
    child_id=random.randrange(95,175,3)
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
    
    return HttpResponseRedirect(reverse('content', args=(id,)))

def is_freeChild(child_id,id):
    if child_id==id:
        return False
    child=UserProfile.objects.get(id=child_id)
    if child.parent_id:
        return False
    return True
