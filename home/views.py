from django.shortcuts import *
from django.contrib.auth.models import *
from django.contrib import messages
from .models import *
from django.contrib.auth.models import User
import uuid
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth import authenticate,login
from django.contrib.auth.decorators import *
# Create your views here.
@login_required(login_url="/")
def home(request):
    return render(request,'home.html')

def login_attempt(request):
     if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user_obj= User.objects.filter(username=username).first() 
        if user_obj is None:
            messages.success(request, "User Not Found.")
            return redirect('/login/')
        profile_obj = profile.objects.filter(user=user_obj).first()
        if not profile_obj.is_verified:
            messages.success(request, "Not a Verified User Check your Mail.")
            return redirect('/login/')
        user=authenticate(username=username,password=password)
        if user is None :
            messages.success(request, "Wrong password, Try again.")
            return redirect('/login/')
        login(request,user)
        return redirect('/')    
     return render(request,'login.html')
 
def register_attempt(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            if User.objects.filter(username=username).first():
                messages.success(request, "Username already exists.")
                return redirect('/register/')
            
            if User.objects.filter(email=email).first():
                messages.success(request, "Email already exists.")
                return redirect('/register/')
            
            user_obj = User.objects.create(username=username, email=email)
            user_obj.set_password(password)
            user_obj.save()
            auth_token=str(uuid.uuid4())
            profile_obj = profile.objects.create(user=user_obj,auth_token=auth_token)
            profile_obj.save()
            send_mail_after_registration(email,auth_token)
            return render(request, 'token_send.html')
        
        except Exception as e:
            print(e)
    
    return render(request, 'register.html')
        
def success_attempt(request):
     return render(request,'success.html')
def token_send(request):
     return render(request,'token_send.html')
 
def send_mail_after_registration(email,token):
    subject='Please verify your email to activate your account'
    message=f'Thank you for creating an account with us. To complete the registration process and activate your account, please click on the link below:http://127.0.0.1:8000/verify/{token}'
    email_from=settings.EMAIL_HOST_USER
    recipient_list=[email]
    send_mail(subject,message,email_from,recipient_list)
    
def verify(request,auth_token):
    try:
         profile_obj = profile.objects.filter(auth_token=auth_token).first()
         if profile_obj.is_verified:
             messages.success(request, "Email is already Verified")
             return redirect('/login/')
         if profile_obj:
             profile_obj.is_verified=True
             profile_obj.save()
             messages.success(request, "Email Verification Successful.")
             return redirect('/login/')
         else:
            return redirect('/error') 
    except Exception as e:
            print(e)
def error_page(request):
    return render(request,'error.html')