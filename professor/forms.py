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


class ProfessorUpdateForm(forms.ModelForm):
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    username = forms.CharField(max_length=30, required=True)
    email = forms.EmailField(max_length=254, required=True)
    department = forms.ModelChoiceField(queryset=Department.objects.all(), required=True)

    class Meta:
        model = Professor
        fields = ('first_name', 'last_name', 'username', 'email', 'department')

    def __init__(self, *args, **kwargs):
        super(ProfessorUpdateForm, self).__init__(*args, **kwargs)
        # Set the initial values based on the existing professor
        self.initial['first_name'] = self.instance.user.first_name
        self.initial['last_name'] = self.instance.user.last_name
        self.initial['username'] = self.instance.user.username
        self.initial['email'] = self.instance.user.email

    def save(self, commit=True):
        # Save the professor-related fields
        professor = super().save(commit=commit)

        # Update the user-related fields
        user = professor.user
        user.username = self.cleaned_data['username']
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.save() 
        # Save the user object
        return super().save(commit=commit)


class ProfessorMyAccountForm(forms.ModelForm):
    username = forms.CharField(max_length=30)
    password1 = forms.CharField(widget=forms.PasswordInput, required=False)
    password2 = forms.CharField(widget=forms.PasswordInput, required=False)

    class Meta:
        model = Professor
        fields = ('username', 'password1')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.initial['username'] = self.instance.user.username
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

        # Remove validation errors for specific fields
        if 'department' in self._errors:
            del self._errors['department']
        if 'is_active' in self._errors:
            del self._errors['is_active']
        if 'first_name' in self._errors:
            del self._errors['first_name']
        if 'last_name' in self._errors:
            del self._errors['last_name']
        if 'email' in self._errors:
            del self._errors['email']
        
        return cleaned_data

    def save(self, commit=True):
        password1 = self.cleaned_data['password1']
        username = self.cleaned_data['username']

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
            if password1:
                user.set_password(password1) 
            user.save()

        return super().save(commit=commit)



