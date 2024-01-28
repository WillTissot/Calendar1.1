from django import forms
from professor.models import Professor
from .models import Course, Department, Semester, CalendarCourse, CalendarSemester, DayChoices

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
    course = forms.ModelChoiceField(queryset=Course.objects.all())
    calendarSemester = forms.ModelChoiceField(queryset=CalendarSemester.objects.all())
    day = forms.ChoiceField(choices=DayChoices.choices)
    is_active = forms.BooleanField(required=False, initial=True)
    is_deleted = forms.BooleanField(required=False, initial=False)
    is_online = forms.BooleanField(required=False, initial=False)


    start_time = forms.TimeField(
        label='Start Time',
        widget=forms.TimeInput(attrs={'type': 'time'}),
    )

    end_time = forms.TimeField(
        label='End Time',
        widget=forms.TimeInput(attrs={'type': 'time'}),
    )

    class Meta:
        model = CalendarCourse
        fields = ['course', 'calendarSemester', 'room_number', 'start_time', 'end_time', 'day', 'is_active', 'is_deleted', 'is_online']

class CalendarCourseProfForm(CalendarCourseForm):
        date = forms.DateField(
        label='Date',
        widget=forms.DateInput(attrs={'type': 'date'}),
        required=False
    )

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.fields['course'].widget.attrs['disabled'] = True
            self.fields['calendarSemester'].widget.attrs['disabled'] = True
            self.fields['day'].widget.attrs['disabled'] = True
            self.fields['is_active'].widget = forms.HiddenInput()
            self.fields['is_deleted'].widget = forms.HiddenInput()

        def clean(self):
            cleaned_data = super().clean()
            
            # Remove validation errors for specific fields
            if 'course' in self._errors:
                del self._errors['course']
            if 'calendarSemester' in self._errors:
                del self._errors['calendarSemester']
            if 'day' in self._errors:
                del self._errors['day']
            
            return cleaned_data


class CalendarSemesterForm(forms.ModelForm):
    semester = forms.ModelChoiceField(queryset=Semester.objects.all(), required=True)

    startDate = forms.DateField(
        label='Start Date',
        widget=forms.DateInput(attrs={'type': 'date'}),
    )

    endDate = forms.DateField(
        label='End Date',
        widget=forms.DateInput(attrs={'type': 'date'}),
    )
    class Meta:
        model = CalendarSemester
        fields = ['semester', 'startDate', 'endDate']

class SemesterForm(forms.ModelForm):
    class Meta:
        model = Semester
        fields = ['year', 'term']
        widgets = {
            'term': forms.Select(choices=Semester.SEMESTER_CHOICES),
        }

