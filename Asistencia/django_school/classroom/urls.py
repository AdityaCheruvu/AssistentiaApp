from django.urls import include, path
from classroom.views import *
from .views import classroom, students, teachers

urlpatterns = [
    path('', classroom.Intital_page, name='Intital_page'),
    path('home/', classroom.home, name='home'),
    path('tpost_form_upload/', classroom.Tpost_form_upload, name='Tpost_form_upload'),
    path('GetAttendanceDetails/', classroom.Details),
    path('individualStudent/', classroom.IndividualStudent, name='IndividualStudent'),
    path('GetStudentDetails/', classroom.AllStudents),
    path('GetStudentDetails1/', classroom.IndividualStudentForStudentLogin),
    path('getDetails/oneStudent/', classroom.OneStudent),
    path('getDetails/allStudents/', classroom.AllStudents1),
    path('getDetails/onParticularDate/', classroom.getDailyAttendance),
    path('takeAttendance/tpost_form_upload/', classroom.TClassDetails),
    path('GetStuOnDate/', classroom.DailyAttendance),
    path('GetStudentDetails1_Date/', classroom.GetStudentDetailsOnDate),
    path('GetDailyAttendance/', classroom.DailyAttendance),
    path('logout/',classroom.logout,name='logout'),
    path('collect_data/',classroom.collect_data),
    path('download/',classroom.download,name='download'),
    path('get_condo_list/',classroom.get_condo_list,name='Condo_List')
]
