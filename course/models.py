from django.db import models


# Create your models here.
class Department(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Semester(models.Model):
    SEMESTER_CHOICES = [
        ('Fall', 'Fall'),
        ('Spring', 'Spring'),
        ('Winter', 'Winter'),
        ('Summer', 'Summer')
    ]
    year = models.IntegerField()
    term = models.CharField(max_length=6, choices=SEMESTER_CHOICES)

    def __str__(self):
        return f"{self.term} {self.year}"

class CalendarSemester(models.Model):
    semester = models.ForeignKey(Semester, on_delete=models.DO_NOTHING)
    startDate = models.DateField()
    endDate = models.DateField()
 
    def __str__(self):
        return f"{self.semester.term} {self.semester.year}"

class DayChoices(models.IntegerChoices):
    MONDAY = 1, 'Monday'
    TUESDAY = 2, 'Tuesday'
    WEDNESDAY = 3, 'Wednesday'
    THURSDAY = 4, 'Thursday'
    FRIDAY = 5, 'Friday'
    SATURDAY = 6, 'Saturday'
    SUNDAY = 7, 'Sunday'

class Course(models.Model):
    code = models.CharField(max_length=10)
    title = models.CharField(max_length=200)
    department = models.ForeignKey(Department, on_delete=models.DO_NOTHING)
    professor = models.ForeignKey('professor.Professor', on_delete=models.DO_NOTHING, default=0)
    credits = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.code} - {self.title}"

class CalendarCourse(models.Model):
    course = models.ForeignKey(Course, on_delete=models.DO_NOTHING)
    calendarSemester = models.ForeignKey(CalendarSemester, on_delete=models.DO_NOTHING, null=True)
    room_number = models.CharField(max_length=10)
    start_time = models.TimeField()
    end_time = models.TimeField()
    day = models.IntegerField(choices=DayChoices.choices, default=DayChoices.SUNDAY)
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    is_online = models.BooleanField(default=False)





