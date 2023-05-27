from django.db import models
from django.contrib.auth.models import User
from course.models import Department, CalendarCourse, Course


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    date_of_birth = models.DateField()
    department = models.ForeignKey(Department, on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.user.get_full_name()

class EnrolledStudentsOnCourse(models.Model):
    course = models.ForeignKey(Course, on_delete=models.DO_NOTHING)
    student = models.ForeignKey(Student, on_delete=models.DO_NOTHING)

class EnrolledStudentsOnCalendarCourse(models.Model):
    calendarCourse = models.ForeignKey(CalendarCourse, on_delete=models.DO_NOTHING)
    student = models.ForeignKey(Student, on_delete=models.DO_NOTHING)
    onCalendar = models.BooleanField(default=False, null=True)