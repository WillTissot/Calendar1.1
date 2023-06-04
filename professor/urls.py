from django.urls import path

from professor.views import professor_create, professor_delete, professor_list, professor_detail, professor_update, request_event_change, Get_Cal_Courses

app_name = "professor"

urlpatterns = [
    path('professors/', professor_list, name='professor_list'),
    path('professor/<int:prof_id>/', professor_detail, name='professor_detail'),
    path('professor/update/<int:prof_id>/', professor_update, name='professor_update'),
    path('professor/create/', professor_create, name='professor_create'),
    path('professor/delete/<int:prof_id>/', professor_delete, name='professor_delete'),
    path('professor/request/change/<int:ev_id>/', request_event_change, name='request_event_change'),
    path('professor/get/calendarcourses/', Get_Cal_Courses, name='get_cal_courses')
]