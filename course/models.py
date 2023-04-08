from django.db import models



# Create your models here.
class Department(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Course(models.Model):
    code = models.CharField(max_length=10)
    title = models.CharField(max_length=200)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    professor = models.ForeignKey('professor.Professor', on_delete=models.CASCADE, default=0)
    credits = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.code} - {self.title}"


class Semester(models.Model):
    SEMESTER_CHOICES = [
        ('Fall', 'Fall'),
        ('Spring', 'Spring'),
        ('Summer', 'Summer')
    ]
    year = models.IntegerField()
    term = models.CharField(max_length=6, choices=SEMESTER_CHOICES)

    def __str__(self):
        return f"{self.term} {self.year}"
