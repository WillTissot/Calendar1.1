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
    start_time = forms.TimeInput()
    end_time = forms.TimeInput()
    day = forms.ChoiceField(choices=DayChoices.choices)
    is_active = forms.BooleanField(required=False, initial=True)
    is_deleted = forms.BooleanField(required=False, initial=False)
    is_online = forms.BooleanField(required=False, initial=False)

    class Meta:
        model = CalendarCourse
        fields = ['course', 'calendarSemester', 'room_number', 'start_time', 'end_time', 'day', 'is_active', 'is_deleted', 'is_online']

class CalendarCourseProfForm(CalendarCourseForm):
        date = forms.DateField(required=False)

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
    startDate = forms.DateField()
    endDate = forms.DateField()

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

