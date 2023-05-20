from django.forms import ModelForm, DateInput
from django import forms
from event.models import Event


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['calendarCourse']