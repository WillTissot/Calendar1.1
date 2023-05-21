from django import forms
from professor.models import Professor
from .models import Course, Department, Semester, CalendarCourse, CalendarSemester

class CourseForm(forms.ModelForm):

    code = forms.CharField(max_length=10, required=True)
    title = forms.CharField(max_length=200, required=True)
    department = forms.ModelChoiceField(queryset=Department.objects.all(), required=True)
    professor = forms.ModelChoiceField(queryset=Professor.objects.all(), required=True)
    credits = forms.IntegerField(required=True)


    class Meta:
        model = Course
        fields = ['code', 'title', 'department', 'professor', 'credits']


class CalendarCourseForm(forms.ModelForm):
    class Meta:
        model = CalendarCourse
        fields = ['course', 'semester', 'room_number', 'start_time', 'end_time', 'day', 'is_active', 'is_deleted', 'is_online']


class CalendarSemesterForm(forms.ModelForm):
    semester = forms.ModelChoiceField(queryset=Semester.objects.all(), required=True)
    startDate = forms.DateField()
    endDate = forms.DateField()

    class Meta:
        model = CalendarSemester
        fields = ['semester', 'startDate', 'endDate']

