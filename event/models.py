from datetime import datetime
from django.db import models
from django.urls import reverse
from course.models import Course, Semester
from professor.models import Professor
from student.models import Student
from course.models import CalendarCourse
from django.contrib.auth.models import User


class Event(models.Model):
    """ Event model """
    calendarCourse = models.ForeignKey(CalendarCourse, on_delete=models.DO_NOTHING, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    
