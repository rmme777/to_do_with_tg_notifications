from django.urls import path
from . import views


# app_name = 'cabinet'

urlpatterns = [
    path('', views.show_cabinet, name='show_cabinet'),
    path('add-notifications', views.bot_redirect_by_token, name='bot_redirect'),
]