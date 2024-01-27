from django.urls import path
from .views import dissertation_create, dissertation_delete, dissertation_detail, dissertation_list, dissertation_update, student_dissertation_list, dissertation_pending_calendar_event_list
from .views import calendardissertation_create, calendardissertation_delete,calendardissertation_detail,calendardissertation_list,calendardissertation_update, create_calendar_dissertation_event

app_name="dissertation"

urlpatterns = [
    path('dissertations/', dissertation_list, name='dissertation_list'),
    path('dissertations1/', dissertation_pending_calendar_event_list, name='dissertation_calendar_create_list'),
    path('dissertations/student/', student_dissertation_list, name='student_dissertation_list'),
    path('dissertation/<int:dissertation_id>/', dissertation_detail, name='dissertation_detail'),
    path('dissertation/update/<int:dissertation_id>/', dissertation_update, name='dissertation_update'),
    path('dissertation/create/', dissertation_create, name='dissertation_create'),
    path('dissertation/delete/<int:dissertation_id>/', dissertation_delete, name='dissertation_delete'),
    path('calendardissertations/', calendardissertation_list, name='calendardissertation_list'),
    path('calendardissertation/<int:calendardissertation_id>/', calendardissertation_detail, name='calendardissertation_detail'),
    path('calendardissertation/update/<int:calendardissertation_id>/', calendardissertation_update, name='calendardissertation_update'),
    path('calendardissertation/create/', calendardissertation_create, name='calendardissertation_create'),
    path('calendardissertation/delete/<int:calendardissertation_id>/', calendardissertation_delete, name='calendardissertation_delete'),
    path('calendardissertation/create/event/<int:calDissertation_id>/', create_calendar_dissertation_event, name='create_calendar_dissertation_event'),
]