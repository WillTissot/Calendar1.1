
from django.urls import path
from course.views import course_create, course_delete, course_detail, course_list, course_update, calendarsemester_create,calendarsemester_delete,calendarsemester_detail,calendarsemester_list,calendarsemester_update
from course.views import calendarcourse_create, calendarcourse_delete, calendarcourse_detail, calendarcourse_list, calendarcourse_update
from course.views import semester_create, semester_delete, semester_detail, semester_list, semester_update
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
    path('calendarCourses/', calendarcourse_list, name='calendarcourse_list'),
    path('calendarCourse/<int:cal_id>/', calendarcourse_detail, name='calendarcourse_detail'),
    path('calendarCourse/update/<int:cal_id>/', calendarcourse_update, name='calendarcourse_update'),
    path('calendarCourse/delete/<int:cal_id>/', calendarcourse_delete, name='calendarcourse_delete'),
    path('calendarCourse/create/', calendarcourse_create, name='calendarcourse_create'),
    path('semesters/', semester_list, name='semester_list'),
    path('semester/<int:sem_id>/', semester_detail, name='semester_detail'),
    path('semester/update/<int:sem_id>/', semester_update, name='semester_update'),
    path('semester/delete/<int:sem_id>/', semester_delete, name='semester_delete'),
    path('semester/create/', semester_create, name='semester_create'),
]