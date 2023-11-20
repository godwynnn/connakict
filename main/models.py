from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    centers=(
        ('umuahia','umuahia'),
        ('aba','aba'),
        ('ohafia','ohafia')
    )
    years=(
        ('2022','2022'),
        ('2023','2023')
    )
    email=models.EmailField(max_length=200,unique=True)
    reg_no=models.CharField(max_length=20,blank=True,null=True)
    center=models.CharField(max_length=20,blank=True,null=True,choices=centers)
    year=models.CharField(max_length=20,blank=True,null=True,choices=years)
    username=models.CharField(max_length=50,blank=True,null=True)
    USERNAME_FIELD='email'
    REQUIRED_FIELDS = ['first_name', 'last_name','password']

    def __str__(self):
        return self.email
    
    def save(self,*args,**kwargs):
        if self.reg_no is not None:
            self.reg_no=self.reg_no.lower()
        else:
            pass
        super().save(*args,**kwargs)
    