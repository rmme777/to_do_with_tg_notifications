from django.urls import path
from . import views


app_name = 'tasks'

urlpatterns = [
    path('', views.view_tasks, name='view_tasks'),
    path('new-task/', views.create_task, name='create_task'),
    path('update-task/<int:task_id>/', views.update_task, name='update_task'),
]