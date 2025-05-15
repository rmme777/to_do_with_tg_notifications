from django.shortcuts import render

def view_tasks(request):
    return render(request, 'tasks/main_tasks.html')
