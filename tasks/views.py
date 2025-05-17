from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import TaskToComplete
from .models import CompletedTask
from django.utils import timezone
from datetime import datetime, time
from django.utils.timezone import make_aware


@login_required
def view_tasks(request):
    if request.method == 'POST':
        task_id = request.POST.get('task_id')
        completed_task_id = request.POST.get('completed_task_id')
        if task_id:
            task = TaskToComplete.objects.get(id=task_id)
            CompletedTask.objects.create(
                task_text=task.task_text,
                task_complete=timezone.now(),
                user_id=task.user_id
            )
            task.delete()
        elif completed_task_id:
            completed_task = CompletedTask.objects.get(id=completed_task_id)
            TaskToComplete.objects.create(
                task_text=completed_task.task_text,
                user_id=completed_task.user_id
            )
            completed_task.delete()

    today = datetime.today().date()
    start = make_aware(datetime.combine(today, time.min))
    end = make_aware(datetime.combine(today, time.max))

    tasks_sorted_by_deadline = TaskToComplete.objects.order_by("-task_deadline")
    tasks_completed_today = CompletedTask.objects.filter(task_complete__range=(start, end))
    return render(request, 'tasks/main_tasks.html', {'tasks': tasks_sorted_by_deadline, 'completed_today': tasks_completed_today})



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
            return redirect('tasks:view_tasks')
    return render(request, 'tasks/add_task.html')

# TODO: добавить возможность в UI быстро добавить обратно задачи выполненные сегодня, например если пользователь случайно выполнил задачу


