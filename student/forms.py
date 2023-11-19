from django import forms

from main.models import User
from . import models
from exam import models as QMODEL

class StudentUserForm(forms.ModelForm):
    class Meta:
        model=User
        fields=['first_name','last_name','password','email','center']
        widgets = {
        'password': forms.PasswordInput()
        }

class StudentForm(forms.ModelForm):
    class Meta:
        model=models.Student
        fields=['mobile','profile_pic']

