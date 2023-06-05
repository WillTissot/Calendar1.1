from django import forms
from .models import Dissertation, CalendarDissertation
from professor.models import Professor


class DissertationForm(forms.ModelForm):
    title = forms.CharField(max_length=500, required=True)
    is_online = forms.BooleanField(required=False)
    is_open_to_public = forms.BooleanField(required=False)
    url = forms.CharField(max_length=1000, required=False)
    supervisor = forms.ModelChoiceField(queryset=Professor.objects.all())
    board = forms.ModelMultipleChoiceField(queryset=Professor.objects.all())
    location = forms.CharField(max_length=1000, required=False)

    class Meta:
        model = Dissertation
        fields = ['title', 'is_online', 'is_open_to_public', 'url', 'supervisor', 'board', 'location']


class CalendarDissertationForm(forms.ModelForm):
    dissertation = forms.ModelChoiceField(queryset=Dissertation.objects.all())
    start_time = forms.TimeInput()
    end_time = forms.TimeInput()
    date = forms.DateInput()

    class Meta:
        model = CalendarDissertation
        fields = ['dissertation', 'start_time', 'end_time', 'date']


class DissertationStudentForm(forms.ModelForm):
    title = forms.CharField(max_length=500, required=True)
    supervisor = forms.ModelChoiceField(queryset=Professor.objects.all())
    board = forms.ModelMultipleChoiceField(queryset=Professor.objects.all())

    class Meta:
        model = Dissertation
        fields = ['title', 'supervisor']