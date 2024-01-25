from django import forms
from course.models import Department
from .models import Professor
from django.contrib.auth.models import User


class ProfessorForm(forms.ModelForm):
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    username = forms.CharField(max_length=30, required=True)
    email = forms.EmailField(max_length=254, required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=True)
    department = forms.ModelChoiceField(queryset=Department.objects.all())

    class Meta:
        model = Professor
        fields = ('first_name', 'last_name', 'username', 'email', 'password', 'department')

    def __init__(self, *args, **kwargs):
        super(ProfessorForm, self).__init__(*args, **kwargs)
        if self.instance.user_id:
            self.initial['first_name'] = self.instance.user.first_name
            self.initial['last_name'] = self.instance.user.last_name
            self.initial['username'] = self.instance.user.username
            self.initial['email'] = self.instance.user.email
            self.initial['password'] = self.instance.user.password

    def save(self, commit=True):
        first_name = self.cleaned_data['first_name']
        last_name = self.cleaned_data['last_name']
        username = self.cleaned_data['username']
        email = self.cleaned_data['email']
        password = self.cleaned_data['password']

        if not self.instance.pk:
            user = User.objects.create_user(
                username=username,
                password=password,
                first_name=first_name,
                last_name=last_name,
                email=email
            )
            self.instance.user = user
        else:
            # Instance already exists, it's an update operation
            user = self.instance.user
            user.username = username
            user.set_password(password)
            user.first_name = first_name
            user.last_name = last_name
            user.email = email
            user.save()

        
        return super().save(commit=commit)



