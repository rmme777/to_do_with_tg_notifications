from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import TaskToComplete
from .models import CompletedTask
from django.utils import timezone


@login_required
def view_tasks(request):
    if request.method == 'POST':
        task_id = request.POST.get('task_id')
        if task_id:
            task = TaskToComplete.objects.get(id=task_id)
            CompletedTask.objects.create(
                task_text=task.task_text,
                task_complete=timezone.now(),
                user_id=task.user_id
            )
            task.delete()

    tasks_sorted_by_deadline = TaskToComplete.objects.order_by("-task_deadline")
    return render(request, 'tasks/main_tasks.html', {'tasks': tasks_sorted_by_deadline})



def create_task(request):
    if request.method == 'POST':
        text = request.POST.get('task_text')
        deadline = request.POST.get('task_deadline')
        if text:
            TaskToComplete.objects.create(
                task_text = text,
                task_deadline = deadline if deadline else None,
                user = request.user
            )
            return redirect('view_tasks')
    return render(request, 'tasks/add_task.html')

# TODO: добавить возможность в UI быстро добавить обратно задачи выполненные сегодня, например если пользователь случайно выполнил задачу


