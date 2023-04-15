from django.urls import path
from .views import student_detail, student_update, student_create, student_list, student_delete


urlpatterns = [
    path('student/<int:det_id>/', student_detail, name='student_detail'),
    path('student/update/<int:up_id>/', student_update, name='student_update'),
    path('student/create/', student_create, name='student_create'),
    path('students/', student_list, name='student_list'),
    path('student/delete/<int:del_id>/', student_delete, name='student_delete'),
]
