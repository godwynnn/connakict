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
    no=models.CharField(max_length=20,blank=True,null=True) 
    year=models.CharField(max_length=20,blank=True,null=True,choices=years)
    username=models.CharField(max_length=50,blank=True,null=True)
    USERNAME_FIELD='email'
    REQUIRED_FIELDS = ['first_name', 'last_name','password']

    def __str__(self):
        return self.email
    
    def save(self,*args,**kwargs):
        if self.no is not None:
            if self.year=='2022':
                if self.center =='aba':
                    self.reg_no=f'CFK/AB/2022/{self.no}'.upper()
                
                if self.center =='umuahia':
                    self.reg_no=f'CFK/UM/2022/{self.no}'.upper()
                
                if self.center =='ohafia':
                    self.reg_no=f'CFK/OH/2022/{self.no}'.upper()
                
                else:
                    pass
            else:
                if self.center =='aba':
                    self.reg_no=f'CFK/AB/2023/{self.no}'.upper()
                
                if self.center =='umuahia':
                    self.reg_no=f'CFK/UM/2023/{self.no}'.upper()
                
                if self.center =='ohafia':
                    self.reg_no=f'CFK/OH/2023/{self.no}'.upper()
                
                else:
                    pass
        else:
            pass
        super().save(*args,**kwargs)
    