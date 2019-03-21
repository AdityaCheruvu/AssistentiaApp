from django.shortcuts import redirect, render
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, render_to_response
from django.utils import timezone
import datetime
from classroom.models import Subject
from classroom.models import User
from classroom.models import ClassToStudent_Mapping
from django.template import RequestContext, loader
from django.template import Template, Context
from django.template.defaulttags import register
from classroom.models import MyModel
from classroom.models import DetailsForm
from classroom.forms import PostForm
from django.http import HttpResponseRedirect
from classroom import MarkAttendanceCode

from classroom.forms import PostForm
import subprocess
from subprocess import call

var1 = ''
cid1=''

def Intital_page(request):
    return render(request, 'classroom/select.html')


#@classroom.route("./classroom/templates/absentees.html", methods=['POST'])
'''def Absentees(request):
            ab=['aditya','pavan','satya','bharath','avinsah']
            some_var = request.POST.getlist('check_1')
            print(some_var)
            return render(request, 'classroom/absentees.html',{'data':ab})'''

def collect_data(request):
        if request.method=='POST':
                plist=request.POST.getlist('present')
                data=request.POST.getlist('check_1')
                classid=request.POST.get('classid')
                userid=request.POST.get('userid')

                print(data)
                print("present list-----")
                print(classid,userid)
                final_result=set(plist+data)
        return render(request,'classroom/collect.html')


class SignUpView(TemplateView):
    template_name = 'registration/signup.html'

@login_required
def home(request):
    if request.user.is_authenticated:
        if request.user.is_teacher:
            global usrname
            usrname = request.user.username
            return render(request, 'classroom/teachers/LecturerLogin.html')
        else:
            return render(request, 'classroom/students/StudentLogin.html')
    return render(request, 'registration/login.html')


class test_code:
    def code(self,classId, UsrName):
        var1 = classId
        print(UsrName)
        print(classId)
        return MarkAttendanceCode.takeAttendance(classId, UsrName) + [classId, UsrName]


    def code1(self, studentID):
        global sid1
        sid1=studentID
        print(sid1)

    def code2(self, classID):
        global cid1
        cid1=classID
        print(cid1)

    '''def collect_data(request):
            if request.method=='POST':
                    data=request.POST.getlist('check_1')
                    print(data)
            return render(request,'classroom/collect.html')'''


def OneStudent(request):
        return render(request, 'classroom/OneStudent.html')

def AllStudents1(request):
        return render(request, 'classroom/AllStudents.html')


def Details(request):
        now = timezone.now()
        users = User.objects.all()
        return render(request, 'classroom/GetAttendnaceDetails.html', {'users': users})

def TClassDetails(request):
        return render(request, 'classroom/TGetClassDetails.html')


def AllStudents(request):
        now = timezone.now()
        if request.method == 'GET':
            form = PostForm()
        else:
            form = PostForm(request.POST)

            if form.is_valid():
                classID = form.cleaned_data['classID']
                py_obj=test_code()
                py_obj.code2(classID)
        print(cid1)
        users = ClassToStudent_Mapping.objects.filter(ClassId = cid1)
        if(bool(users)):
            return render(request, 'classroom/AllStudentDetails.html', {'users': users})
        else:
            return render(request, 'classroom/None.html', {'users': users})

def IndividualStudentForStudentLogin(request):
        now = timezone.now()
        users = User.objects.all()
        return render(request, 'classroom/IndividualStudentDetailsForStudentLogin.html', {'users': users})


def IndividualStudent(request):
        now = timezone.now()
        if request.method == 'GET':
            form = PostForm()
        else:
            form = PostForm(request.POST)

            if form.is_valid():
                studentID = form.cleaned_data['classID']
                py_obj=test_code()
                py_obj.code1(studentID)
        users = User.objects.filter(username = sid1)
        if(bool(users)):
            return render(request, 'classroom/IndividualStudentDetails.html', {'users': users})
        else:
            return render(request, 'classroom/None.html', {'users': users})


def Tpost_form_upload(request):
    if request.method == 'GET':
        form = PostForm()
    else:
        form = PostForm(request.POST)
        usrname = request.user.username

        if form.is_valid():
            classID = form.cleaned_data['classID']
            py_obj=test_code()
            data=py_obj.code(classID, usrname)
            print(data[0],data[1],data[2],data[3])
    return render(request, 'classroom/absentees.html',{'data':list(data[0]),'data1':list(data[1]),'classId':data[2],'usrname':data[3]})
