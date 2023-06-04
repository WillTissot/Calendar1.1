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
    path('professor/events/<int:ev_id>/get/changes/', views.get_changes, name='get_changes'),
    path('event/detail/<int:ev_id>/', views.event_detail, name='event_detail'),
    path('event/update/<int:ev_id>/', views.event_update, name='event_update'),
    path('event/delete/<int:ev_id>/', views.event_delete, name='event_delete'),
    path('event/create/calendar/event/<int:cal_id>/', views.create_calendar_event, name='create_calendar_event'),
    path('secretary/events/changes/action/', views.get_all_requests, name='get_all_requests'),
    path('secretary/users/approve', views.validate_user, name='users_approve'),
]