from django.shortcuts import redirect, render
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, render_to_response
from django.utils import timezone
import datetime
from django.contrib import messages

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
import csv
from classroom.forms import PostForm
import subprocess
from subprocess import call
from django.contrib.auth.decorators import login_required
from django.contrib import auth
from django.conf import settings
from django.http import HttpResponse,Http404
import xlsxwriter
var1 = ''
cid1=''
sid_d=''
date_d=''

def Intital_page(request):
    return render(request, 'classroom/select.html')


@login_required
def logout(request):
        auth.logout(request)
        return redirect('login')


#@classroom.route("./classroom/templates/absentees.html", methods=['POST'])
'''def Absentees(request):
            ab=['aditya','pavan','satya','bharath','avinsah']
            some_var = request.POST.getlist('check_1')
            print(some_var)
            return render(request, 'classroom/absentees.html',{'data':ab})'''

def get_condo_list(request):
    return render(request,'classroom/Get_condo_list.html')

def Hod_Attendnace(request):
    if request.user.is_authenticated:
        return render(request, 'classroom/DownloadAttendanceDetails.html')
    else:
        return render(request, 'classroom/NotAuthenticated.html')

#@permission_required('admin.can_add_log_entry')
def download(request):
    response=HttpResponse(content_type='text/csv')
    response['Content-Disposition']='attachment;filename="attendence_list.xlsx"'
    if request.method=='POST':
        cid=request.POST.get('classID')
        cid1 = cid.lower();
        print(cid1)
        usrname = request.user.username
        usrname1 = usrname.lower();
        x = usrname1.split('_')
        cid2 = cid1[1:len(cid1)-1]
        if(cid2 == x[1]):
            try:
                        users = MarkAttendanceCode.getCumulativeAttendanceOfStudents(cid)
                        print(users)
                        if(len(users)==0):
                                            return render(request, 'classroom/None.html')
                        else:
                            workbook = xlsxwriter.Workbook(response)
                            worksheet = workbook.add_worksheet()
                            cell_format = workbook.add_format()
                            cell_format.set_bold()
                            cell_format.set_font_color('red')
                            row =0
                            col=0
                            count=0
                            for user in users:
                                for  data in  user:
                                        if count==0:
                                                    worksheet.write(row, col,data,cell_format)
                                        worksheet.write(row, col,data)
                                        col +=1
                                        if count!=0 and int(user[-1]) < 75:
                                                cc=0
                                row += 1
                                col=0
                                count+=1
                            workbook.close()

            except IndexError:
                        return render(request, 'classroom/None.html')
            return response
        else:
            return render(request, 'classroom/NotAuthenticated.html')
            return response


def contact(request):
    return render(request,'classroom/contact.html')
def collect_data(request):
    if request.user.is_authenticated:
        if request.user.is_teacher:
            if request.method=='POST':
                    studentToClassMap = MACObj.getStudenToClassMap()
                    plist = request.POST.getlist('present')
                    data=request.POST.getlist('check_1')
                    classid=request.POST.get('classid')
                    userid=request.POST.get('userid')
                    print(data)
                    print("present list-----")
                    print(classid,userid)
                    print(plist)
                    print(data)
                    print(studentToClassMap)
                    final_result=set(plist+data)
                    print(final_result)
                    classToStudent = {}
                    for i in final_result:
                        try:
                            classToStudent[studentToClassMap[i]].append(i)
                        except:
                            classToStudent[studentToClassMap[i]] = [i]
                    for classid, final_result in classToStudent.items():
                        MarkAttendanceCode.updateInDB(classid, userid, final_result)
            return render(request,'classroom/collect.html')
        else:
            return render(request, 'classroom/NotAuthenticated.html')


class SignUpView(TemplateView):
    template_name = 'registration/signup.html'


@login_required
def home(request):
    if request.user.is_authenticated:
        if request.user.is_teacher:
            global usrname
            usrname = request.user.username
            return render(request, 'classroom/teachers/LecturerLogin.html')
        elif request.user.is_student:
            global stuUsrname
            stuUsrname = request.user.username
            return render(request, 'classroom/students/StudentLogin.html')
        else:
            global hodUsrname
            hodUsrname = request.user.username
            return render(request, 'classroom/Hod/HodLogin.html')
    return render(request, 'registration/login.html')


class test_code:
    def code(self,classId, UsrName):
        var1 = classId
        print(UsrName)
        print(classId)
        global MACObj
        MACObj = MarkAttendanceCode.AttendanceTake()
        classIds = MarkAttendanceCode.getClassesFromElective(classId, UsrName)
        print("ClassIDs = ", classIds)
        return MACObj.takeAttendance(classIds, UsrName) + [classId, UsrName]


    def code1(self, studentID):
        global sid1
        sid1=studentID
        print(sid1)

    def code2(self, classID):
        global cid1
        cid1=classID
        print(cid1)

    def code3(self, studentId, Date):
        global sid_d
        global date_d
        sid_d=studentId
        date_d = Date

    '''def collect_data(request):
            if request.method=='POST':
                    data=request.POST.getlist('check_1')
                    print(data)
            return render(request,'classroom/collect.html')'''


def OneStudent(request):
    if request.user.is_authenticated:
        if request.user.is_teacher:
            return render(request, 'classroom/OneStudent.html')
        else:
            return render(request, 'classroom/NotAuthenticated.html')

def AllStudents1(request):
    if request.user.is_authenticated:
        if request.user.is_teacher:
            return render(request, 'classroom/AllStudents.html')
        else:
            return render(request, 'classroom/NotAuthenticated.html')


def Details(request):
    if request.user.is_authenticated:
        if request.user.is_teacher:
            now = timezone.now()
            users = User.objects.all()
            return render(request, 'classroom/GetAttendnaceDetails.html', {'users': users})
        else:
            return render(request, 'classroom/NotAuthenticated.html')

def TClassDetails(request):
    if request.user.is_authenticated:
        if request.user.is_teacher:
            return render(request, 'classroom/TGetClassDetails.html')
        else:
            return render(request, 'classroom/NotAuthenticated.html')

def AllStudents(request):
        now = timezone.now()
        if request.method == 'GET':
            form = PostForm()
        else:
            form = PostForm(request.POST)
            classID = form['classID'].value()
            py_obj=test_code()
            py_obj.code2(classID)
        print("Cid is " + cid1)
        #users = ClassToStudent_Mapping.objects.filter(ClassId = cid1)
        try:
            users = MarkAttendanceCode.getCumulativeAttendanceOfStudents(cid1)
            try:
                print(users[1])
            except:
                return render(request, 'classroom/None_cid.html', {'message':'Enter Valid ClassId'})
        except IndexError:
            return render(request, 'classroom/None_cid.html', {'message':'Enter Valid ClassId'})
        if(bool(users)):
            return render(request, 'classroom/AllStudentDetails.html', {'users': users, 'classId' : cid1})
        else:
            return render(request, 'classroom/None_cid.html', {'users': users, 'message':'Enter Valid ClassId'})

def GetStudentDetailsOnDate(request):
    if request.user.is_authenticated:
        return render(request, 'classroom/GetStudentDetailsOnDate.html')
    else:
        return render(request, 'classroom/NotAuthenticated.html')



def IndividualStudentForStudentLogin(request):
    if request.user.is_authenticated:
        if request.user.is_student:
            now = timezone.now()
            #users = User.objects.all()
            try:
                users = MarkAttendanceCode.getCumulativeAttendanceOfAStudent(stuUsrname)
            except IndexError:
                return render(request, 'classroom/None.html')
            print(users)
            return render(request, 'classroom/IndividualStudentDetailsForStudentLogin.html', {'users': users})
        else:
            return render(request, 'classroom/NotAuthenticated.html')

def getDailyAttendance(request):
    if request.user.is_authenticated:
        if request.user.is_teacher:
            return render(request, 'classroom/dailyAttendance.html')
        else:
            return render(request, 'classroom/NotAuthenticated.html')

def DailyAttendance(request):
    now = timezone.now()
    if request.method == 'GET':
        form = PostForm()
    else:
        form = PostForm(request.POST)
        if request.user.is_teacher:
            if form.is_valid():
                studentID = form.cleaned_data['classID']
                print(studentID)
                date1 = form.cleaned_data['Date']
                py_obj=test_code()
                py_obj.code3(studentID, date1)
        else:
            form = PostForm(request.POST)
            studentID = request.user.username
            print(studentID)
            date1 = form['classID'].value()
            print(date1)
            py_obj=test_code()
            py_obj.code3(studentID, date1)
    #users = ClassToStudent_Mapping.objects.filter(ClassId = cid1)
    try:
        users = MarkAttendanceCode.getDailyAttendance(studentID, date1)
    except IndexError:
        return render(request, 'classroom/None_date.html', {'message':'Enter Valid Details'})
    if(bool(users)):
        paramList=[studentID+" on ", date1]
        print(paramList)
        return render(request, 'classroom/IndividualStudentDetails.html', {'users': users, 'param':paramList})
    else:
        return render(request, 'classroom/None_date.html', {'users': users, 'message':'Enter Valid Details'})

def IndividualStudent(request):
        now = timezone.now()
        if request.method == 'GET':
            form = PostForm()
        else:
            form = PostForm(request.POST)
            studentID = form['classID'].value()
            py_obj=test_code()
            py_obj.code1(studentID)
        try:
            users = MarkAttendanceCode.getCumulativeAttendanceOfAStudent(studentID)
        except IndexError:
            return render(request, 'classroom/None.html', {'message':'Enter Valid StudentId'})
        print(users);
        #users = User.objects.filter(username = sid1)
        if(bool(users)):
            return render(request, 'classroom/IndividualStudentDetails.html', {'users': users, 'sid':studentID})
        else:
            return render(request, 'classroom/None.html', {'users': users})


def Tpost_form_upload(request):
    if request.user.is_authenticated:
        if request.user.is_teacher:
            if request.method == 'GET':
                form = PostForm()
            else:
                form = PostForm(request.POST)
                usrname = request.user.username

                classID = form['classID'].value()
                py_obj=test_code()
                data=py_obj.code(classID, usrname)
                print(data[0],data[1],data[2],data[3])
                MarkAttendanceCode.callAbsenteesListAloud(list(data[0]))
            return render(request, 'classroom/absentees.html',{'data':list(data[0]),'data1':list(data[1]),'classId':data[2],'usrname':data[3]})
        else:
            return render(request, 'classroom/NotAuthenticated.html')
