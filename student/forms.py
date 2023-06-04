from django import forms
from django.contrib.auth.models import User
from course.models import Department
from .models import Student
from django.shortcuts import get_object_or_404


class SimpleStudentForm(forms.ModelForm):
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    username = forms.CharField(max_length=30, required=True)
    email = forms.EmailField(max_length=254, required=True)
    date_of_birth = forms.DateField(widget=forms.TextInput(attrs={'type': 'date'}))
    department = forms.ModelChoiceField(queryset=Department.objects.all())
    is_active = forms.BooleanField()

    class Meta:
        model = Student
        fields = ('first_name', 'last_name', 'username', 'email', 'date_of_birth', 'department')


    def __init__(self, *args, **kwargs):
        super(SimpleStudentForm, self).__init__(*args, **kwargs)
        # Set initial values for User fields from related User model
        if self.instance.user_id:
            self.initial['first_name'] = self.instance.user.first_name
            self.initial['last_name'] = self.instance.user.last_name
            self.initial['username'] = self.instance.user.username
            self.initial['email'] = self.instance.user.email
            self.initial['is_active'] = self.instance.user.is_active

    def save(self, commit=True):
        first_name = self.cleaned_data['first_name']
        last_name = self.cleaned_data['last_name']
        username = self.cleaned_data['username']
        email = self.cleaned_data['email']
        is_active = self.cleaned_data['is_active']

        if not self.instance.pk:
            user = User.objects.create_user(
                username=username,
                first_name=first_name,
                last_name=last_name,
                email=email,
                is_active=is_active
            )
            self.instance.user = user
        else:
            # Instance already exists, it's an update operation
            user = self.instance.user
            user.username = username
            #user.set_password(password)
            user.first_name = first_name
            user.last_name = last_name
            user.email = email
            user.is_active = is_active
            user.save()

        
        return super().save(commit=commit)

class StudentForm(SimpleStudentForm):
    password = forms.CharField(max_length=30, required=False)

    class Meta:
        model = Student
        fields = ('first_name', 'last_name', 'username', 'password', 'email', 'date_of_birth', 'department')

    def __init__(self, *args, **kwargs):
        super(StudentForm, self).__init__(*args, **kwargs)
        # Set initial values for User fields from related User model
        if self.instance.user_id:
            self.initial['password'] = None

    def clean_password(self):
        password = self.cleaned_data['password']
        if not password and not self.instance.pk:
            raise forms.ValidationError('Password is required')
        return password
    def save(self, commit=True):
        password = self.cleaned_data['password']
        first_name = self.cleaned_data['first_name']
        last_name = self.cleaned_data['last_name']
        username = self.cleaned_data['username']
        email = self.cleaned_data['email']
        is_active = self.cleaned_data['is_active']

        if not self.instance.pk:
            user = User.objects.create_user(
                username=username,
                first_name=first_name,
                password=password,
                last_name=last_name,
                email=email,
                is_active=is_active
            )
            self.instance.user = user
        else:
            # Instance already exists, it's an update operation
            user = self.instance.user
            user.username = username
            user.first_name = first_name
            user.last_name = last_name
            user.email = email
            user.is_active = is_active
            if password:
                user.set_password(password) 
            user.save()

        
        return super().save(commit=commit)

class StudentMyAccountForm(SimpleStudentForm):
    username = forms.CharField(max_length=30)
    password1 = forms.CharField(widget=forms.PasswordInput, required=False)
    password2 = forms.CharField(widget=forms.PasswordInput, required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['department'].widget.attrs['disabled'] = True
        self.fields['is_active'].widget.attrs['disabled'] = True
        self.fields['date_of_birth'].widget.attrs['disabled'] = True
        self.fields['first_name'].widget.attrs['disabled'] = True
        self.fields['last_name'].widget.attrs['disabled'] = True
        self.fields['email'].widget.attrs['disabled'] = True
        self.initial['password1'] = None
        self.initial['password2'] = None

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and not password2:
            raise forms.ValidationError('Please confirm your password')
        elif password1 and password2 and password1 != password2:
            raise forms.ValidationError('Passwords do not match')
        return password2

    def clean(self):
        cleaned_data = super().clean()

        preserved_fields = ['department', 'is_active', 'date_of_birth', 'first_name', 'last_name', 'email']
        
        for field in preserved_fields:
            if field in self.fields and field in self.initial:
                if field == 'department':
                    cleaned_data[field] = get_object_or_404(Department, id = self.initial[field])
                else:
                    cleaned_data[field] = self.initial[field]


        # Remove validation errors for specific fields
        if 'department' in self._errors:
            del self._errors['department']
        if 'is_active' in self._errors:
            del self._errors['is_active']
        if 'date_of_birth' in self._errors:
            del self._errors['date_of_birth']
        if 'first_name' in self._errors:
            del self._errors['first_name']
        if 'last_name' in self._errors:
            del self._errors['last_name']
        if 'email' in self._errors:
            del self._errors['email']
        
        return cleaned_data

    def save(self, commit=True):
        password1 = self.cleaned_data['password1']
        first_name = self.cleaned_data['first_name']
        last_name = self.cleaned_data['last_name']
        username = self.cleaned_data['username']
        email = self.cleaned_data['email']
        is_active = self.cleaned_data['is_active']

        if not self.instance.pk:
            user = User.objects.create_user(
                username=username,
                first_name=first_name,
                password=password1,
                last_name=last_name,
                email=email,
                is_active=is_active
            )
            self.instance.user = user
        else:
            # Instance already exists, it's an update operation
            user = self.instance.user
            user.username = username
            user.first_name = first_name
            user.last_name = last_name
            user.email = email
            user.is_active = is_active
            if password1:
                user.set_password(password1) 
            user.save()

        
        return super().save(commit=commit)