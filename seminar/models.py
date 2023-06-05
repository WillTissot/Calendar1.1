from django.db import models
from student.models import Student

# Create your models here.
class Seminar(models.Model):
    title = models.CharField(max_length=500)
    is_online = models.BooleanField(default=False)
    url = models.CharField(max_length=1000, null=True)
    speaker_fullname = models.CharField(max_length=500)
    location = models.CharField(max_length=1000, null=True)

    def __str__(self):
        return f"{self.title}"

class CalendarSeminar(models.Model):
    seminar = models.ForeignKey(Seminar, on_delete=models.DO_NOTHING)
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    onCalendar = models.BooleanField(null=True)


class EnrolledStudentToCalendarSeminars(models.Model):
    calendarSeminar = models.ForeignKey(CalendarSeminar, on_delete=models.DO_NOTHING)
    students = models.ManyToManyField(Student)