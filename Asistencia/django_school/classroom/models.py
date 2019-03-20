from __future__ import unicode_literals
from django.contrib.auth.models import AbstractUser
from django.db import models

from django.forms import ModelForm
from django.utils.html import escape, mark_safe



class User(AbstractUser):
    is_student = models.BooleanField(default=False)
    is_teacher = models.BooleanField(default=False)


class Subject(models.Model):
    name = models.CharField(max_length=30)
    color = models.CharField(max_length=7, default='#007bff')

    def __str__(self):
        return self.name

    def get_html_badge(self):
        name = escape(self.name)
        color = escape(self.color)
        html = '<span class="badge badge-primary" style="background-color: %s">%s</span>' % (color, name)
        return mark_safe(html)


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)

    def __str__(self):
        return self.user.username


Dep_Choices=((1,'CSE'),(2,'ECE'),(3,'EIE'),('4','MECH'),('5','CIV'),)
Year_Choices=((1,'I'),(2,'II'),(3,'III'),(4,'IV'),)
Sec_Choices=((1,'1'),(2,'2'),(3,'3'),(4,'4'),)

class MyModel(models.Model):
	year=models.CharField(max_length=6,choices=Year_Choices,default=None)
	department=models.CharField(max_length=6,choices=Dep_Choices,default=None)
	section=models.CharField(max_length=6,choices=Sec_Choices,default=None)

class DetailsForm(ModelForm):

	class Meta:
		model=MyModel
		fields=['year','department','section']

class Event(models.Model):
     name = models.CharField('Event Name', max_length=120)
     event_date = models.DateTimeField('Event Date')
     venue = models.CharField(max_length=120)
     manager = models.CharField(max_length = 60)
     description = models.TextField(blank=True)

class ClassToStudent_Mapping(models.Model):
    ClassId = models.TextField('Class ID')
    RollNo = models.TextField('Roll Number')

    def __str__(self):
        return self.ClassId

    def __str__(self):
        return self.RollNo

class ClassToSub_Mapping(models.Model):
    ClassId = models.TextField('ClassID')
    SubId = models.IntegerField('SubId')
    SubName = models.TextField('SubName')

class CumulativeAttendance(models.Model):
    RollNo = models.TextField('Roll Number')
    SubId = models.IntegerField('SubId')
    Attended = models.IntegerField('Attended')

class CumulativeAttendanceTotal(models.Model):
    ClassId = models.TextField('ClassID')
    SubId = models.IntegerField('SubId')
    Total = models.IntegerField('Attended')


class DailyAttendance(models.Model):
    RollNo = models.TextField('Roll Number')
    Date_c = models.DateField('Date')
    SubId = models.IntegerField('SubId')
    Attended = models.IntegerField('Attended')


class DailyAttendanceTotal(models.Model):
    ClassId = models.TextField('ClassID')
    Date_c = models.DateField('Date')
    SubId = models.IntegerField('SubId')
    Total = models.IntegerField('Attended')

class ProfToSubMapping(models.Model):
    ClassId = models.TextField('Class ID')
    RollNo = RollNo = models.TextField('Roll Number')
    Prof = models.TextField('Professor')
    SubId = models.IntegerField('SubId')
