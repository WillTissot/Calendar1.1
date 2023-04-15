from django.urls import reverse
from django.views.generic import View
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login

from .forms import SignInForm

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
            print("form valid")
            email = forms.cleaned_data["email"]
            password = forms.cleaned_data["password"]
            user = authenticate(request, username=email, password=password)
            print(user)
            if user:
                login(request, user)
                print("Successful login")
                return redirect("student:student_list")
        context = {"form": forms}
        return render(request, self.template_name, context)