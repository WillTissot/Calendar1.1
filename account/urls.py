from django.urls import path

from . import views

app_name = "accounts"


urlpatterns = [
    path("studentsignup/", views.student_signup, name="studentsignup"),
    path("professorsignup/", views.professor_signup, name="professorsignup"),
    path("logout/", views.signout, name="logout"),
    path("signin/", views.SignInView.as_view(), name="signin"),
    path("myprofile/", views.see_my_profile, name="myprofile"),
    #path("signout/", views.signout, name="signout"),
    #path("redirect-to-other-app/", views.redirect_to_other_app, name="student")
    #path('redirect/', views.SignInForm, name='student'),
]   