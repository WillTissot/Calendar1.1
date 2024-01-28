from django import forms
from .models import Dissertation, CalendarDissertation
from professor.models import Professor
from student.models import Student


class DissertationForm(forms.ModelForm):
    title = forms.CharField(max_length=500, required=True)
    is_online = forms.BooleanField(required=False)
    is_open_to_public = forms.BooleanField(required=False)
    url = forms.CharField(max_length=1000, required=False)
    supervisor = forms.ModelChoiceField(queryset=Professor.objects.all())
    board = forms.ModelMultipleChoiceField(queryset=Professor.objects.all())
    location = forms.CharField(max_length=1000, required=False)
    is_approved = forms.BooleanField(required=False)
    student = forms.ModelChoiceField(Student.objects.all())


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['student'].widget.attrs['disabled'] = True

    def clean(self):
        cleaned_data = super().clean()
        
        if 'student' in self._errors:
            del self._errors['student']

    class Meta:
        model = Dissertation
        fields = ['title', 'is_online', 'is_open_to_public', 'url', 'supervisor', 'board', 'location', 'is_approved', 'student']



class CalendarDissertationForm(forms.ModelForm):
    dissertation = forms.ModelChoiceField(queryset=Dissertation.objects.all())
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


    def __init__(self, *args, dissertation=None, **kwargs):
        super().__init__(*args, **kwargs)
        if dissertation:
            self.fields['dissertation'].initial = dissertation
            self.fields['dissertation'].widget.attrs['readonly'] = True

    class Meta:
        model = CalendarDissertation
        fields = ['dissertation', 'start_time', 'end_time', 'date']


class DissertationStudentForm(forms.ModelForm):
    title = forms.CharField(max_length=500, required=True)
    supervisor = forms.ModelChoiceField(queryset=Professor.objects.all())
    board = forms.ModelMultipleChoiceField(queryset=Professor.objects.all())

    class Meta:
        model = Dissertation
        fields = ['title', 'supervisor', 'board']