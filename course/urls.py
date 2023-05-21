
from django.urls import path
from course.views import course_create, course_delete, course_detail, course_list, course_update, calendarsemester_create,calendarsemester_delete,calendarsemester_detail,calendarsemester_list,calendarsemester_update

app_name = "course"

urlpatterns = [
    path('courses/', course_list, name='course_list'),
    path('course/<int:cou_id>/', course_detail, name='course_detail'),
    path('course/update/<int:cou_id>/', course_update, name='course_update'),
    path('course/create/', course_create, name='course_create'),
    path('course/delete/<int:cou_id>/', course_delete, name='course_delete'),
    path('calendarSemesters/', calendarsemester_list, name='calendarSemester_list'),
    path('calendarSemester/<int:sem_id>/', calendarsemester_detail, name='calendarSemester_detail'),
    path('calendarSemester/update/<int:sem_id>/', calendarsemester_update, name='calendarSemester_update'),
    path('calendarSemester/delete/<int:sem_id>/', calendarsemester_delete, name='calendarSemester_delete'),
    path('calendarSemester/create/', calendarsemester_create, name='calendarSemester_create'),
]