from django.urls import reverse
from django.views.generic import View
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login

from .forms import ProfessorSignUpForm, SignInForm, StudentSignUpForm

class SignInView(View):
    """ User registration view """

    template_name = "./signin.html"
    form_class = SignInForm

    def get(self, request, *args, **kwargs):
        forms = self.form_class()
        context = {"form": forms}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        forms = self.form_class(request.POST)
        if forms.is_valid():
            username = forms.cleaned_data["username"]
            password = forms.cleaned_data["password"]
            user = authenticate(request, username=username, password=password)
            print(user)
            if user:
                login(request, user)
                print("Successful login")
                return redirect("event:dashboard")
        context = {"form": forms}
        return render(request, self.template_name, context)
    
def student_signup(request):
    if request.method == 'POST':
        form = StudentSignUpForm(request.POST)
        if form.is_valid():
            student = form.save()
            return redirect('student:student_detail', det_id=student.pk)
    else:
        form = StudentSignUpForm()
    return render(request, 'signup.html', {'form': form})

def professor_signup(request):
    if request.method == 'POST':
        form = ProfessorSignUpForm(request.POST)
        if form.is_valid():
            professor = form.save()
            return redirect('professor:professor_detail', prof_id=professor.pk)
    else:
        form = StudentSignUpForm()
    return render(request, 'signup.html', {'form': form})