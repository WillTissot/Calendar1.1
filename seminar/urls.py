from django.urls import path
from .views import seminar_create, seminar_delete, seminar_detail, seminar_list, seminar_update
from .views import calendarseminar_create, calendarseminar_delete, calendarseminar_detail, calendarseminar_list, calendarseminar_update, enroll_to_calendar_seminar

app_name="seminar"

urlpatterns = [
    path('seminars/', seminar_list, name='seminar_list'),
    path('seminar/<int:seminar_id>/', seminar_detail, name='seminar_detail'),
    path('seminar/update/<int:seminar_id>/', seminar_update, name='seminar_update'),
    path('seminar/create/', seminar_create, name='seminar_create'),
    path('seminar/delete/<int:seminar_id>/', seminar_delete, name='seminar_delete'),
    path('calendarseminars/', calendarseminar_list, name='calendarseminar_list'),
    path('calendarseminar/<int:calSeminar_id>/', calendarseminar_detail, name='calendarseminar_detail'),
    path('calendarseminar/update/<int:calSeminar_id>/', calendarseminar_update, name='calendarseminar_update'),
    path('calendarseminar/create/', calendarseminar_create, name='calendarseminar_create'),
    path('calendarseminar/delete/<int:calSeminar_id>/', calendarseminar_delete, name='calendarseminar_delete'),
    path('calendarseminar/attend/', enroll_to_calendar_seminar, name='enroll_to_calendar_seminar'),
    
]