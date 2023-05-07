from django import forms

from professor.models import Professor
from .models import Course, Department, Semester

class CourseForm(forms.ModelForm):

    code = forms.CharField(max_length=10, required=True)
    title = forms.CharField(max_length=200, required=True)
    department = forms.ModelChoiceField(queryset=Department.objects.all(), required=True)
    professor = forms.ModelChoiceField(queryset=Professor.objects.all(), required=True)
    credits = forms.IntegerField(required=True)


    class Meta:
        model = Course
        fields = ['code', 'title', 'department', 'professor', 'credits']
