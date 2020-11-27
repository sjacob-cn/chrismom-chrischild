from django.shortcuts import render,redirect
from django.http import HttpResponse,HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from .models import UserProfile,Comment,Reply
from django.contrib.auth.models import User
from django.urls import reverse
import random

@csrf_exempt
@login_required(login_url='/accounts/login/')
def dashboard(request):
    user_id = request.user.id
   
    b = UserProfile.objects.get(id= user_id)
    
    if b.is_password_reset == False :
        b.is_password_reset = True
        b.save()
        return redirect('password_change')

    if request.user.id:
        print(request.user.id)
        userprofile=UserProfile.objects.get(id=request.user.id)
        u = User.objects.all()
        q=UserProfile.objects.all()
        obj={'userprofile':userprofile,'u':u,'q':q,'UserProfile':UserProfile.objects.all()}
        return render(request, "user/dashboard.html",obj)
    else:
        print('logging out')
        return render(request, "user/dashboard.html")
    
    
    
@csrf_exempt
@login_required(login_url='/accounts/login/')
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
@csrf_exempt
@login_required(login_url='/accounts/login/')
def chat(request):
    # user=UserProfile.objects.get(id=95)
    
    return render(request,'user/commentbox.html',{'comments':Comment.objects.all()})
@csrf_exempt
@login_required(login_url='/accounts/login/')
def reply(request,id):
    text=str(request.POST.get('reply'))
    print('sample text ',text)
    if text !="" and  text.split()!=[]:
        rep=Reply(comment=Comment.objects.get(id=id),user=User.objects.get(id=(id+94)),comments=text)
        #reason for id+94-->user table id starts with 95

        rep.save()
        print('saved')
    return HttpResponseRedirect(reverse('chat'))

@csrf_exempt
@login_required(login_url='/accounts/login/')
def comment(request):
    print('welcome')
    
    
    sender=str(request.POST.get('user'))
    print(sender)
    text=request.POST.get('comment')
    if text !="" and  text.split()!=[]:
        if sender != 'anonymous':
            com=Comment(user=User.objects.get(id=int(request.user.id)),comment=request.POST.get('comment'),sender=sender)
        else:
            com=Comment(user=User.objects.get(id=int(request.user.id)),comment=request.POST.get('comment'))

        com.save()
        print('saved')
    return HttpResponseRedirect(reverse('chat'))



