from django.shortcuts import render,redirect
from . import forms,models
from django.db.models import Sum
from django.contrib.auth.models import Group
from django.http import HttpResponseRedirect,JsonResponse,HttpResponse
from django.contrib.auth.decorators import login_required,user_passes_test
from django.conf import settings
from datetime import date, timedelta
from exam import models as QMODEL
from teacher import models as TMODEL
from django.core.exceptions import ObjectDoesNotExist
from django.urls import reverse,reverse_lazy
from exam.decorators import student_exam_check
import random
#for showing signup/login button for student
def studentclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request,'student/studentclick.html')

def student_signup_view(request):
    userForm=forms.StudentUserForm()
    studentForm=forms.StudentForm()
    mydict={'userForm':userForm,'studentForm':studentForm}
    if request.method=='POST':
        userForm=forms.StudentUserForm(request.POST or None)
        studentForm=forms.StudentForm(request.POST or None,request.FILES or None)
        if userForm.is_valid() and studentForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            student=studentForm.save(commit=False)
            student.user=user
            student.save()
            my_student_group = Group.objects.get_or_create(name='STUDENT')
            my_student_group[0].user_set.add(user)
        return HttpResponseRedirect('studentlogin')
    return render(request,'student/studentsignup.html',context=mydict)

def student_login(request):
    pass

def is_student(user):
    return user.groups.filter(name='STUDENT').exists()

@login_required(login_url='studentlogin')
@user_passes_test(is_student)
def student_dashboard_view(request):
    dict={
    
    'total_course':QMODEL.Course.objects.all().count(),
    'total_question':QMODEL.Question.objects.all().count(),
    
    }
    return render(request,'student/student_dashboard.html',context=dict)

@login_required(login_url='studentlogin')
@user_passes_test(is_student)

def student_exam_view(request):

    courses=QMODEL.Course.objects.all()
    
    context={}
    objects=QMODEL.Result.objects.filter(student__user=request.user,submitted=True)
    result=list(map(lambda x:x.exam,objects))
    # print(object)
    # result=[]
    # for obj in objects:
    #     result.append(obj.exam)

    context['courses']=courses
    context['submitted']=result
    # print(context)
    
    return render(request,'student/student_exam.html',context)


def exam_redirect(request):
    ref_id=request.GET.get('ref_id')
    try:
        course=QMODEL.Course.objects.get(ref_id=ref_id)
        print(course)
        return HttpResponseRedirect(reverse('take-exam',args=[course.id]))


    except ObjectDoesNotExist:
        return HttpResponse('page not found')



@login_required(login_url='studentlogin')
@user_passes_test(is_student)
@student_exam_check
def take_exam_view(request,pk):
    course=QMODEL.Course.objects.get(id=pk)
    total_questions=QMODEL.Question.objects.all().filter(course=course).count()
    questions=QMODEL.Question.objects.all().filter(course=course)
    total_marks=0
    for q in questions:
        total_marks=total_marks + q.marks
    
  
    return render(request,'student/take_exam.html',{'course':course,'total_questions':total_questions,'total_marks':total_marks})




import datetime
@login_required(login_url='studentlogin')
@user_passes_test(is_student)
@student_exam_check
def start_exam_view(request,pk):
    # student=QMODEL.Student.objects.get(user=request.user)
    course=QMODEL.Course.objects.get(id=pk)
    timer,created=QMODEL.Timer.objects.get_or_create(
        course=course,
        student=request.user.student
    )
    # print(datetime.datetime.now()-timer.end_time_date)
    questions=list(QMODEL.Question.objects.all().filter(course=course))
    random.shuffle(questions)
    if request.method=='POST':
        pass
    response= render(request,'student/start_exam.html',{'course':course,'questions':questions,'timer':timer.end_time_date})
    if request.COOKIES.get('course_id') is not None:
        if int(request.COOKIES.get('course_id')) != pk:
            return HttpResponse('<h3>Have an unfinished exam session ongoing, please complete it before accessing another</h3>')
            # course_id=request.COOKIES.get('course_id')
            # return redirect('start-exam',kwargs={'pk':int(course_id)})
    else:
        response.set_cookie('course_id',course.id)
    return response


@login_required(login_url='studentlogin')
@user_passes_test(is_student)
def calculate_marks_view(request):
    if request.COOKIES.get('course_id') is not None:
        course_id = request.COOKIES.get('course_id')
        course=QMODEL.Course.objects.get(id=course_id)
        
        total_marks=0
        questions=QMODEL.Question.objects.all().filter(course=course)
        for i in range(len(questions)):
            
            selected_ans = request.COOKIES.get(str(i+1))
            # print(request.COOKIES)
            # print(selected_ans)
            actual_answer = questions[i].answer
            if selected_ans == actual_answer:
                total_marks = total_marks + questions[i].marks
        student = models.Student.objects.get(user_id=request.user.id)
        result = QMODEL.Result()
        result.marks=total_marks
        result.exam=course
        result.student=student
        result.submitted=True
        result.save()

        # HttpResponse.delete_cookie('course_id')

        response = HttpResponseRedirect('view-result')
        response.delete_cookie('course_id')
        return response



@login_required(login_url='studentlogin')
@user_passes_test(is_student)
def view_result_view(request):
    courses=QMODEL.Course.objects.all()
    return render(request,'student/view_result.html',{'courses':courses})
    

@login_required(login_url='studentlogin')
@user_passes_test(is_student)
def check_marks_view(request,pk):
    course=QMODEL.Course.objects.get(id=pk)
    student = models.Student.objects.get(user_id=request.user.id)
    results= QMODEL.Result.objects.all().filter(exam=course).filter(student=student)
    return render(request,'student/check_marks.html',{'results':results})

@login_required(login_url='studentlogin')
@user_passes_test(is_student)
def student_marks_view(request):
    courses=QMODEL.Course.objects.all()
    return render(request,'student/student_marks.html',{'courses':courses})
  
