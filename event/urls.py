from . import views
from django.urls import path

app_name = 'event'

urlpatterns = [
    path("calender/", views.CalendarViewNew.as_view(), name="calendar"),
]