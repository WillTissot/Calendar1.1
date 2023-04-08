from django import forms
from django.contrib.auth.models import User
from course.models import Department
from .models import Student

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ('user', 'date_of_birth', 'department')
        
    user = forms.ModelChoiceField(queryset=User.objects.all())
    date_of_birth = forms.DateField(widget=forms.TextInput(attrs={'type': 'date'}))
    department = forms.ModelChoiceField(queryset=Department.objects.all())
