from django.contrib import admin
from .models import TaskToComplete, CompletedTask

admin.site.register(TaskToComplete)
admin.site.register(CompletedTask)

