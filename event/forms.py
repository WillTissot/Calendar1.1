from django.forms import ModelForm, DateInput
from django import forms
from event.models import Event
from course.models import CalendarCourse
from seminar.models import CalendarSeminar
from dissertation.models import CalendarDissertation


class EventForm(forms.ModelForm):

    room_number = forms.CharField(max_length=30)
    is_online = forms.BooleanField()

    calendarCourse = forms.ModelChoiceField(queryset=CalendarCourse.objects.all())
    calendarSeminar = forms.ModelChoiceField(queryset=CalendarSeminar.objects.all())
    calendarDissertation = forms.ModelChoiceField(queryset=CalendarDissertation.objects.all())

    start_time = forms.TimeField(
        label='Start Time',
        widget=forms.TimeInput(attrs={'type': 'time'}),
    )

    end_time = forms.TimeField(
        label='End Time',
        widget=forms.TimeInput(attrs={'type': 'time'}),
    )

    date = forms.DateField(
        label='Date',
        widget=forms.DateInput(attrs={'type': 'date'}),
    )


    def __init__(self, *args, calendarCourse=None, calendarSeminar=None, calendarDissertation=None, **kwargs):
        super().__init__(*args, **kwargs)
       
        last = self.instance.changes.filter(is_approved=True, is_pending=False).order_by('-date_created').first()

        if self.instance:
            self.initial['start_time'] = last.start_time
            self.initial['end_time'] = last.end_time
            self.initial['date'] = last.date
            self.initial['room_number'] = last.room_number
            self.initial['is_online'] = last.is_online


        if calendarCourse:
            self.fields['calendarCourse'].initial = calendarCourse
            self.fields['calendarCourse'].widget.attrs['disabled'] = True
            self.fields['calendarSeminar'].widget = forms.HiddenInput()
            self.fields['calendarDissertation'].widget = forms.HiddenInput()


        if calendarSeminar:
            self.fields['calendarSeminar'].initial = calendarSeminar
            self.fields['calendarSeminar'].widget.attrs['disabled'] = True
            self.fields['calendarCourse'].widget = forms.HiddenInput()
            self.fields['calendarDissertation'].widget = forms.HiddenInput()

        if calendarDissertation:
            self.fields['calendarDissertation'].initial = calendarDissertation
            self.fields['calendarDissertation'].widget.attrs['disabled'] = True
            self.fields['calendarCourse'].widget = forms.HiddenInput()
            self.fields['calendarSeminar'].widget = forms.HiddenInput()

    class Meta:
        model = Event
        fields = ['calendarCourse', 'calendarSeminar', 'calendarDissertation', 'room_number', 'start_time', 'end_time', 'is_online',  'date']