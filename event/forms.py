from django.forms import ModelForm, DateInput
from django import forms
from course.models import Course, Semester

from event.models import Event
from professor.models import Professor



class EventForm(forms.ModelForm):
    class Meta:
        course = forms.ModelChoiceField(queryset=Course.objects.all(), required=True)
        semester = forms.ModelChoiceField(queryset=Semester.objects.all(), required=True)
        room_number = forms.CharField(max_length=10)
        start_time = forms.DateTimeField(widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}))
        end_time = forms.DateTimeField(widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}))
        is_active = forms.BooleanField(required=False)
        is_deleted = forms.BooleanField(required=False)
        is_online = forms.BooleanField(required=False)
        professor = forms.ModelChoiceField(queryset=Professor.objects.all(), required=True)
        fields = ['professor', 'course', 'semester', 'room_number', 'start_time', 'end_time', 'is_active', 'is_deleted', 'is_online']
        widgets = {
            'start_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'end_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }
    class Meta:
        model = Event
        fields = ['professor', 'course', 'semester', 'room_number', 'start_time', 'end_time', 'is_active', 'is_deleted', 'is_online']
