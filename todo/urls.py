"""
URL configuration for todo project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from registration.forms import AuntieficationForm


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', auth_views.LoginView.as_view(template_name='registration/login.html', authentication_form=AuntieficationForm), name='login'),
    path('tasks/', include(('tasks.urls', 'tasks'), namespace='tasks')),
    path('account/', include('django.contrib.auth.urls')),
    path('register/', include('registration.urls')),

]

# git commit -m "Initial commit. Added apps: registration, tasks, cabinet. Migrated tables 'users' with django's built-in LoginView, completed_tasks, tasks_to_complete. Added login form in app registration. Added template for main page with login."
