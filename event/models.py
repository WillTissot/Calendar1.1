from datetime import datetime
from django.db import models
from django.urls import reverse
from course.models import Course, Semester
from professor.models import Professor
from student.models import Student
from course.models import CalendarCourse
from django.contrib.auth.models import User
from dataclasses import dataclass
from enum import Enum


class Event(models.Model):
    """ Event model """
    calendarCourse = models.ForeignKey(CalendarCourse, on_delete=models.DO_NOTHING, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


@dataclass
class DayMonth:
    day: int
    month: int

class DateTimeEnum(Enum):
    DATE1 = DayMonth(25, 12)
    DATE2 = DayMonth(26, 12)
    DATE3 = DayMonth(1, 1)
    DATE4 = DayMonth(6, 1)
    DATE5 = DayMonth(30, 1)
    DATE6 = DayMonth(25, 3)
    DATE7 = DayMonth(15, 8)
    DATE8 = DayMonth(28, 10)
    DATE9 = DayMonth(17, 11)




    
