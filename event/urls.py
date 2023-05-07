from . import views
from django.urls import path

app_name = 'event'

urlpatterns = [
    path('myevents/', views.event_list, name='event_list'),
    path('mydashboard/', views.dashboard, name='dashboard'),
    path('', views.homepage, name='homepage'),
    path('adminpage/', views.adminpage, name='adminpage')
]