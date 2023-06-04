from django import forms
from .models import Seminar


class SeminarForm(forms.ModelForm):
    title = forms.CharField(max_length=500, required=True)
    is_online = forms.BooleanField(required=False)
    url = forms.CharField(max_length=1000, required=False)
    speaker_fullname = forms.CharField(max_length=500, required=True)
    location = forms.CharField(max_length=1000, required=False)

    class Meta:
        model = Seminar
        fields = ['title', 'is_online', 'url', 'speaker_fullname', 'location']