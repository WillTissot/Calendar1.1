from django.db import models
from professor.models import Professor
from student.models import Student

# Create your models here.

class Dissertation(models.Model):
    title = models.CharField(max_length=200)
    is_online = models.BooleanField(default=False)
    is_open_to_public = models.BooleanField(default=False)
    url = models.CharField(max_length=1000, null=True)
    supervisor = models.ForeignKey(Professor, on_delete=models.DO_NOTHING, related_name='supervisor_professor')
    board = models.ManyToManyField(Professor, related_name='board_professors')
    location = models.CharField(max_length=1000, null=True)
    is_approved = models.BooleanField(null=True)
    student = models.ForeignKey(Student, on_delete=models.DO_NOTHING, null=True)

    def __str__(self):
        return f"{self.title}"

class CalendarDissertation(models.Model):
    dissertation = models.ForeignKey(Dissertation, on_delete=models.DO_NOTHING)
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()





