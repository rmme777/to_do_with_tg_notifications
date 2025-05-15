from django.urls import path
from . import views

urlpatterns = [
    path('', views.view_tasks, name='view_tasks'),
]