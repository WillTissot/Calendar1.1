from django.urls import path

from professor.views import professor_list


urlpatterns = [
    path('professors/', professor_list, name='professor_list')
]