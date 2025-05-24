from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .models import TaskToComplete
from .models import CompletedTask
from django.utils import timezone
from datetime import datetime, time, timedelta
from django.utils.timezone import make_aware
from django.utils.dateparse import parse_datetime
from cabinet.models import NotificationBot


@login_required
def view_tasks(request):
    valid_minutes = [5, 15, 30, 60]
    saved_task_id = None
    try:
        notif_bot = NotificationBot.objects.get(user=request.user)
        notifications_enabled = notif_bot.notifications_included
    except NotificationBot.DoesNotExist:
        notifications_enabled = False

    if request.method == 'POST':
        task_id = request.POST.get('task_id')
        completed_task_id = request.POST.get('completed_task_id')
        delete_task_id = request.POST.get('to_delete_task_id')
        save_notification_task_id = request.POST.get('save_notification_task_id')

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


        elif delete_task_id:
            to_delete = TaskToComplete.objects.get(id=delete_task_id)
            to_delete.delete()


        elif save_notification_task_id:
            task = TaskToComplete.objects.get(id=save_notification_task_id)
            selected = request.POST.get('notification_time')

            if selected == 'custom':
                custom_minutes = int(request.POST.get('custom_minutes', 0))
                delta = timedelta(minutes=custom_minutes)
            else:
                delta = timedelta(minutes=int(selected))

            task.notification_time = task.task_deadline - delta
            task.save()

            saved_task_id = task.id

    today = datetime.today().date()
    start = make_aware(datetime.combine(today, time.min))
    end = make_aware(datetime.combine(today, time.max))
    tasks_sorted_by_deadline = TaskToComplete.objects.order_by("-task_deadline")
    tasks_completed_today = CompletedTask.objects.filter(task_complete__range=(start, end))

    for task in tasks_sorted_by_deadline:
        if task.task_deadline and task.notification_time:
            delta = (task.task_deadline - task.notification_time).total_seconds() // 60
            task.notification_delta_minutes = int(delta)
        else:
            task.notification_delta_minutes = None

    return render(request, 'tasks/main_tasks.html', {
        'tasks': tasks_sorted_by_deadline,
        'completed_today': tasks_completed_today,
        'valid_minutes': valid_minutes,
        'saved_task_id': saved_task_id,
        'notifications_enabled': notifications_enabled,
    })


@login_required
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

@login_required
def update_task(request, task_id):

    task = get_object_or_404(TaskToComplete, id=task_id, user=request.user)

    if request.method == 'POST':
        task_text = request.POST.get('task_text')
        task_deadline = request.POST.get('task_deadline')

        if task_text:
            task.task_text = task_text

        if task_deadline:
            task.task_deadline = parse_datetime(task_deadline)
        else:
            task.task_deadline = None

        task.save()
        return redirect('tasks:view_tasks')

    return render(request, 'tasks/update_task.html', {'task': task})

