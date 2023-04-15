from django.urls import path

from . import views

app_name = "accounts"


urlpatterns = [
    #path("signup/", views.SignUpView.as_view(), name="signup"),
    path("signin/", views.SignInView.as_view(), name="signin"),
    #path("signout/", views.signout, name="signout"),
    #path("redirect-to-other-app/", views.redirect_to_other_app, name="student")
    #path('redirect/', views.SignInForm, name='student'),
]   