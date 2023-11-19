from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    centers=(
        ('umuahia','umuahia'),
        ('aba','aba'),
        ('ohafia','ohafia')
    )
    email=models.EmailField(max_length=200,unique=True)
    reg_no=models.CharField(max_length=20,blank=True,null=True)
    center=models.CharField(max_length=20,blank=True,null=True,choices=centers)
    

    USERNAME_FIELD='email'
    REQUIRED_FIELDS = ['first_name', 'last_name','password']

    def __str__(self):
        return self.email
    