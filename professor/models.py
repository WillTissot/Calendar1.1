from django.contrib.auth.models import User
from django.db import models
from course.models import Department


# Create your models here.

class Professor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.get_full_name()
