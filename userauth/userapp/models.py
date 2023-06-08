from django.db import models
from .models import *
from django.contrib.auth.models import User
# Create your models here.
class profile(models.Model):
    User=models.OneToOneField(User,on_delete=models.CASCADE)
    auth_token=models.CharField(max_length=20)
    is_verified=models.BooleanField(default=False)
    created_at=models.DateTimeField(auto_now_add=True)