from django.urls import path

from professor.views import professor_list, professor_detail


urlpatterns = [
    path('professors/', professor_list, name='professor_list'),
    path('professor/<int:det_id>/', professor_detail, name='professor_detail'),
    #path('student/update/<int:up_id>/', professor_update, name='professor_update'),
    #path('student/create/', professor_create, name='professor_create'),
    #path('student/delete/<int:del_id>/', professor_delete, name='professor_delete')
]