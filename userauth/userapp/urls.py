from django.contrib import admin
from django.urls import path,include
from .views import *
urlpatterns = [

    path('',register),
    path('success/',success),
    path('error/',error),
    path('verify/<auth_token>',verify),
    path('send_mail_register/',send_mail_register),
    path('login/',login)


]