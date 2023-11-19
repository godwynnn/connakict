from django.db import models
import datetime
from student.models import Student
from django.utils import timezone


class Course(models.Model):
   
   course_name = models.CharField(max_length=50)
   question_number = models.PositiveIntegerField()
   total_marks = models.PositiveIntegerField()
   hr_duration=models.IntegerField(null=True,blank=True,default=0)
   min_duration=models.IntegerField(null=True,blank=True,default=0)
   ref_id=models.CharField(max_length=500,null=True,blank=True)
   

   def __str__(self):
        return self.course_name
   def save(self,*args,**Kwargs):
        if self.hr_duration is None:
           self.hr_duration=0
        if self.min_duration is None:
           self.min_duration=0

        super().save(*args,**Kwargs)

class Timer(models.Model):
    student = models.ForeignKey(Student,on_delete=models.CASCADE,null=True,blank=True)
    course=models.ForeignKey(Course,on_delete=models.CASCADE)
    end_time_date=models.DateTimeField(null=True,blank=True)

    def save(self,*args,**Kwargs):
        if self.end_time_date is None:
            self.end_time_date=datetime.datetime.now()+datetime.timedelta(minutes=self.course.min_duration,hours=self.course.hr_duration)
        

        super().save(*args,**Kwargs)

class Question(models.Model):

    
    course=models.ForeignKey(Course,on_delete=models.CASCADE,null=True,blank=True)
    marks=models.PositiveIntegerField()
    question=models.CharField(max_length=600)
    extra_desc=models.TextField(max_length=600,null=True,blank=True)
    option1=models.TextField(max_length=200,null=True,blank=True)
    option2=models.TextField(max_length=200,null=True,blank=True)
    option3=models.TextField(max_length=200,null=True,blank=True)
    option4=models.TextField(max_length=200,null=True,blank=True)
    ref_id=models.CharField(max_length=500,null=True,blank=True)
    cat=(('Option1','Option1'),('Option2','Option2'),('Option3','Option3'),('Option4','Option4'))
    answer=models.CharField(max_length=200,choices=cat)

    options=(
        ('0','obj'),
        ('1','practical')
    )
    category=models.CharField(max_length=100,choices=options,null=True)

    def __str__(self):
        return f'{self.course.course_name.upper()} - {self.question}'

class Result(models.Model):
    student = models.ForeignKey(Student,on_delete=models.CASCADE)
    exam = models.ForeignKey(Course,on_delete=models.CASCADE)
    passed=models.BooleanField(default=False)
    submitted=models.BooleanField(default=False)
    marks = models.PositiveIntegerField()
    date = models.DateTimeField(auto_now=True)


    def __str__(self):
        return f'RESULT of {self.student.user.email} for {self.exam.course_name} '
    

