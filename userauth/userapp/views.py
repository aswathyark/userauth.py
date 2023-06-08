import uuid

from django.conf.global_settings import EMAIL_HOST_USER
from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.http import HttpResponse
from django.shortcuts import render, redirect

from .models import *


# Create your views here.
def send_mail_register(email,token):
    subject="your account has been verified"
    message=f'pass the link to verify your account http://127.0.0.1:8000/verify/{token}'
    email_from=EMAIL_HOST_USER
    recipient=[email]
    send_mail(subject,message,email_from,recipient)
def verify(request,auth_token):
    profile_obj=profile.objects.filter(auth_token=auth_token).first()
    if profile_obj:
        if profile_obj.is_verified:
            messages.success(request,'your account alredy verified')
            redirect(login)
        profile_obj.is_verified=True
        profile_obj.save()
        messages.success(request,'ur account verified')
        return redirect(login)
    else:
        return redirect(error)
def error(request):
    return render(request,"error.html")




def login(request):
    global User
    if request.method=='POST':
        uname=request.POST.get('uname')
        pas=request.POST.get('password')
        user_obj=User.objects.filter(username=uname).first()
        if user_obj is None:
            messages.success(request,'user not found')
            return redirect(login)
        profile_obj=profile.objects.filter(User=user_obj).first()
        if not profile_obj.is_verified:
            messages.success(request,'profile not verified,check ur mail')
            return redirect(login)
        User=authenticate(username=uname,password=pas)
        if User is None:
            messages.success(request,'wrong password or username')
            return redirect(login)
        return HttpResponse("success")
    return render(request,'login.html')
def register(request):
    if request.method=="POST":
        uname=request.POST.get('uname')
        email=request.POST.get('email')
        pas=request.POST.get('password')
        if User.objects.filter(username=uname).first():
            messages.success(request,"username taken")
            return redirect(register)
        if User.objects.filter(email=email).first():
            messages.success(request,"email taken")
            return redirect(register)
        user_obj=User(username=uname,email=email)
        user_obj.set_password(pas)
        user_obj.save()
        auth_token=str(uuid.uuid4())
        profile_obj=profile.objects.create(User=user_obj,auth_token=auth_token)
        profile_obj.save()
        send_mail_register(email,auth_token)
        return redirect(success)
    return render(request,"register.html")
def success(request):
    return render(request,"success.html")