from django.shortcuts import render,redirect
from django.http import HttpResponse,HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from .models import UserProfile,Comment,Reply
from django.contrib.auth.models import User
from django.urls import reverse
from .forms import ContactForm
import random
import string
from django.core.mail import send_mail, BadHeaderError
import smtplib,ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import secrets
from django.contrib.auth import authenticate



@csrf_exempt
@login_required(login_url='/accounts/login/')
def dashboard(request):
    user_id = request.user.id
   
    profile = UserProfile.objects.get(id= user_id)
    
    if profile.is_password_reset == False :
        profile.is_password_reset = True
        profile.save()
        return redirect('password_change')

    if user_id:
        #logging in
        userprofile=UserProfile.objects.get(id=user_id)
        users = User.objects.all()
        profiles=UserProfile.objects.all()
        objects={'userprofile':userprofile,'u':users,'q':profiles,'UserProfile':UserProfile.objects.all()}
        return render(request, "user/dashboard.html",objects)
    else:
        #logging out
        return render(request, "user/dashboard.html")
    
    
    
@csrf_exempt
@login_required(login_url='/accounts/login/')
def content(request,id):
    user=UserProfile.objects.get(id=id)
    users = User.objects.all()
    profiles=UserProfile.objects.all()
    objects={'user':user,'u':users,'q':profiles,'UserProfile':UserProfile.objects.all()}
    return render(request,'user/content.html',objects)

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
    
    users = User.objects.all()
    return render(request,'user/commentbox.html',{'comments':Comment.objects.all(),'u':users})

@csrf_exempt
@login_required(login_url='/accounts/login/')
def reply(request,id):
    text=str(request.POST.get('reply'))
    
    if text !="" and  text.split()!=[]:
        reply=Reply(comment=Comment.objects.get(id=id),user=User.objects.get(id=(id+94)),comments=text)
        #reason for id+94-->user table id starts with 95

        reply.save()
        
    return HttpResponseRedirect(reverse('chat'))

@csrf_exempt
@login_required(login_url='/accounts/login/')
def comment(request):
    receiver=int(request.POST.get('menu'))
    text=request.POST.get('comment')
    if text !="" and  text.split()!=[]:
        comments=Comment(user=User.objects.get(id=int(request.user.id)),comment=request.POST.get('comment'),receiver=receiver)
        comments.save()
    return HttpResponseRedirect(reverse('chat'))

def passwordreset(request):
    if request.method == 'GET':
        form = ContactForm()
        
    else:

        form = ContactForm(request.POST)
        
        if form.is_valid():
            
            from_email = form.cleaned_data['from_email']
            #Object creation for User Table 
            a = User.objects.filter(email=from_email).first()
            
           
            if a != None:
                
                user_id = a.id
                #Object creation for UserProfile Table
                c = UserProfile.objects.get(user_id = user_id)
                c.is_password_reset = False
                c.save()
                N = 7 #size of the random string

                #random password generation
                rand = ''.join(random.choices(string.ascii_uppercase + string.digits, k = N))

                #Object creation for User Table
                d = User.objects.get(id = user_id)

                new_password = 'Christmas'+rand
                d.set_password(new_password)
                d.save()
                print(new_password)
                
                #Sending email for password reset
                try:
                    message = "Hi " + d.username +"\n \nYou are receiving this email because you requested a password reset for your Condenast Christmas Account ("+ d.email +"). \nPlease login your account with the password: "+ new_password +"\n \nNote: Please change your password after login.\n \nHave a nice day!! \n \n \nRegards \nCondeNast Christmas Team"
                    send_mail('Conde Christmas | Password Reset' , message , 'Condenast Christmas Event' , [from_email])
                except BadHeaderError:
                    return HttpResponse('Invalid header found.')
                return redirect('password_reset_done')    
        
    
    return render(request, "registration/passwordreset.html", {'form': form})

@login_required(login_url='/accounts/login/')
def viewTasks(request):

    comments=Comment.objects.filter(receiver=request.user.id)
    tasks='<ol>'

    for comment in comments:
        tasks+="<center><li>"+comment.comment+"</li></center>"
    tasks+='</ol>'
    return HttpResponse(tasks)