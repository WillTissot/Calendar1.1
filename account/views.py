from django.urls import reverse
from django.views.generic import View
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

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
                if user.is_superuser:
                    return redirect("event:adminpage")
                else:
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

    context = {
        'form' : form,
        'is_stud' : True
    }
    return render(request, 'signup.html', context)

def professor_signup(request):
    if request.method == 'POST':
        form = ProfessorSignUpForm(request.POST)
        if form.is_valid():
            professor = form.save()
            return redirect('professor:professor_detail', prof_id=professor.pk)
    else:
        form = ProfessorSignUpForm()

    context = {
        'form' : form,
        'is_prod' : True
    }
    return render(request, 'signup.html', context)

@login_required
def signout(request):
    logout(request)
    return redirect('event:homepage')

@login_required
def see_my_profile(request):
    user = request.user
    if hasattr(user, 'student'):
        return redirect('student:student_detail', det_id=user.student.pk)
    else:
        return redirect('professor:professor_detail', prof_id=user.professor.pk)