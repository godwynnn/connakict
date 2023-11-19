from django.shortcuts import redirect,HttpResponse
from exam.models import *
def Authenticated_User(view_func):
    def wrapper_func(request,*args,kwargs):
        if args[0].user.is_authenticated:
            return redirect('')
           


def student_exam_check(view_func):
    def wrapper_func(request,*args,**kwargs):
        # print(kwargs)
        course=Course.objects.get(id=kwargs['pk'])
        submitted=[]
        results=Result.objects.filter(student__user=request.user,submitted=True)
        for result in results:
            submitted.append(result.exam)
        if course in submitted:
            return redirect('afterlogin')
        else:

            return view_func(request,*args,**kwargs)
    
    return wrapper_func