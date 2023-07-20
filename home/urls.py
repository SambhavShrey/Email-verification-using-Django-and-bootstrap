from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [
    path('', home, name="home"),
    path('login/', login_attempt, name="login_attempt"),
    path('register/', register_attempt, name="register_attempt"),
    path('success/', success_attempt, name="success_attempt"),
    path('token_send/', token_send, name="token_send"),
    path('verify/<auth_token>', verify, name="verify"),
     path('error', error_page, name="error"),
]
