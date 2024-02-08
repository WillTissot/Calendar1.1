import base64
from django.urls import reverse
from django.views.generic import View
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core import signing
from django.contrib.auth import login, get_user_model
from django.shortcuts import redirect, get_object_or_404
from django.views.decorators.http import require_GET
from django.utils import timezone
from urllib.parse import urlencode
from django.core.mail import send_mail
from datetime import date, timedelta, datetime
from .forms import ProfessorSignUpForm, SignInForm, StudentSignUpForm

User = get_user_model()

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
            if user:
                login(request, user)
                if user.is_superuser:
                    return redirect("event:adminpage")
                else:
                    return redirect("event:dashboard")
            else:
                message = "Invalid username/password or you account is not authenticated yet!"
                
        context = {
            'form' : forms,
            'message' : message
            }
        return render(request, self.template_name, context)
    
def student_signup(request):
    if request.method == 'POST':
        form = StudentSignUpForm(request.POST)
        if form.is_valid():
            student = form.save()
            return redirect('event:homepage')
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
            return redirect('event:homepage')
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


@require_GET
def magic_link_login(request):
    token = request.GET.get("token")
    if not token:
        # Go back to main page; alternatively show an error page
        return redirect("/")

    # Max age of 15 minutes
    try:
        data = signing.loads(token, max_age=900)
    except signing.SignatureExpired:
        # signature expired, redirect to main page or show error page.
        return redirect("/")

    email = data.get("email")
    if not email:
        return redirect("/")

    user = User.objects.filter(email=email, is_active=True).first()
    if not user:
        # user does not exist or is inactive
        return redirect("/")

    # we want to make sure
    # it's only been generated since the last login
    if user.last_login:
        token_timestamp = signing.b62_decode(token.split(":")[1])
        if token_timestamp < user.last_login.timestamp():
            return redirect("event:dashboard")

    # Everything checks out, log the user in and redirect to dashboard!
    login(request, user)

    return redirect("event:dashboard")




def home(request):
    if request.POST:
        email = request.POST.get("email")

        # if the user exists, send them an email
        if user := User.objects.filter(email=email, is_active=True).first():
            token = signing.dumps({"email": email})
            qs = urlencode({"token": token})

            magic_link = request.build_absolute_uri(
                location=reverse("accounts:auth-magic-link"),
            ) + f"?{qs}"

            # send email
            send_mail(
                "Login link",
                f'Click <a href="{magic_link}">here</a> to login',
                'from@example.com',
                [email],
                fail_silently=True,
            )
        return redirect("/")
    return render(request, 'link_login.html', {})

