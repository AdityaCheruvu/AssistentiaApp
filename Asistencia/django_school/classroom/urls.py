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
    path('takeAttendance/tpost_form_upload/', classroom.TClassDetails),
    path('absentees/',classroom.Absentees,name='absentees'),
]
