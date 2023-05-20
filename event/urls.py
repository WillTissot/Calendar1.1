from . import views
from django.urls import path

app_name = 'event'

urlpatterns = [
    path('myevents/', views.event_list, name='my_event_list'),
    path('mydashboard/', views.dashboard, name='dashboard'),
    path('', views.homepage, name='homepage'),
    path('adminpage/', views.adminpage, name='adminpage'),
    path('secretary/events/', views.sec_event_list, name='sec_event_list'),
    path('secretary/events/<int:ev_id>/get/students/', views.get_students, name='get_students'),
    path('event/detail/<int:ev_id>/', views.event_detail, name='event_detail'),
    path('event/update/<int:ev_id>/', views.event_update, name='event_update'),
    path('event/delete/<int:ev_id>/', views.event_delete, name='event_delete'),
]