from django.urls import path
from .views import seminar_create, seminar_delete, seminar_detail, seminar_list, seminar_update

app_name="seminar"

urlpatterns = [
    path('seminars/', seminar_list, name='seminar_list'),
    path('seminar/<int:seminar_id>/', seminar_detail, name='seminar_detail'),
    path('seminar/update/<int:seminar_id>/', seminar_update, name='seminar_update'),
    path('seminar/create/', seminar_create, name='seminar_create'),
    path('seminar/delete/<int:seminar_id>/', seminar_delete, name='seminar_delete'),
]