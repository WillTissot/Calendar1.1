from datetime import datetime
from django.db import models
from django.urls import reverse
from course.models import Course, Semester
from professor.models import Professor
from student.models import Student
from django.contrib.auth.models import User


class Event(models.Model):
    """ Event model """

    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="events", null=True)
    professor = models.ForeignKey(Professor, on_delete=models.CASCADE, related_name="events", null=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE)
    room_number = models.CharField(max_length=10)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    is_online = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

# class EventManager(models.Manager):
#     """ Event manager """

#     def get_all_events(self, user):
#         events = Event.objects.filter(user=user, is_active=True, is_deleted=False)
#         return events

#     def get_running_events(self, user):
#         running_events = Event.objects.filter(
#             user=user,
#             is_active=True,
#             is_deleted=False,
#             end_time__gte=datetime.now().date(),
#         ).order_by("start_time")
#         return running_events

    
