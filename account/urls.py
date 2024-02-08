from django.urls import path

from . import views

app_name = "accounts"


urlpatterns = [
    path("studentsignup/", views.student_signup, name="studentsignup"),
    path("professorsignup/", views.professor_signup, name="professorsignup"),
    path("logout/", views.signout, name="logout"),
    path("signin/", views.SignInView.as_view(), name="signin"),
    path("signin_second/", views.home, name="signin_link"),
    path('auth/magic-link/', views.magic_link_login, name='auth-magic-link'),
    
]   