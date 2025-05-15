from django.urls import path
from . import views

urlpatterns = [
    path('', views.user_register, name='user_register'),
]
