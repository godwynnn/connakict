from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    email=models.EmailField(max_length=200,unique=True)
    reg_no=models.CharField(max_length=20,blank=True,null=True)
    center=models.CharField(max_length=20,blank=True,null=True)

    USERNAME_FIELD='email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    def __str__(self):
        return self.email
    