from django.urls import path
from .views import dissertation_create, dissertation_delete, dissertation_detail, dissertation_list, dissertation_update
from .views import calendardissertation_create, calendardissertation_delete,calendardissertation_detail,calendardissertation_list,calendardissertation_update

app_name="dissertation"

urlpatterns = [
    path('dissertations/', dissertation_list, name='dissertation_list'),
    path('dissertation/<int:dissertation_id>/', dissertation_detail, name='dissertation_detail'),
    path('dissertation/update/<int:dissertation_id>/', dissertation_update, name='dissertation_update'),
    path('dissertation/create/', dissertation_create, name='dissertation_create'),
    path('dissertation/delete/<int:dissertation_id>/', dissertation_delete, name='dissertation_delete'),
    path('calendardissertations/', calendardissertation_list, name='calendardissertation_list'),
    path('calendardissertation/<int:calendardissertation_id>/', calendardissertation_detail, name='calendardissertation_detail'),
    path('calendardissertation/update/<int:calendardissertation_id>/', calendardissertation_update, name='calendardissertation_update'),
    path('calendardissertation/create/', calendardissertation_create, name='calendardissertation_create'),
    path('calendardissertation/delete/<int:calendardissertation_id>/', calendardissertation_delete, name='calendardissertation_delete'),
]