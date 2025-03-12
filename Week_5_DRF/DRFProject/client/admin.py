from django.contrib import admin
from django.db import models

# Register your models here.

class UserOrder(models.Model):
    name=models.CharField(max_length=50)
    
