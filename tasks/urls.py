from django.urls import path
from . import views




urlpatterns = [
    path('', views.view_tasks, name='view_tasks'),
    path('new-task/', views.create_task, name='create_task'),
]