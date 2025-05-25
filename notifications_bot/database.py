from zoneinfo import ZoneInfo
from asgiref.sync import sync_to_async


def django_db_setup():
    import os
    import django
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'todo.settings')
    django.setup()


django_db_setup()
from cabinet.models import NotificationBot
from tasks.models import TaskToComplete, CompletedTask




@sync_to_async
def get_from_notifbot_by_token(uuid_token):
    """
    Asynchronous data retrieval from model NotificationBot by uuid_token
    """
    try:
        return NotificationBot.objects.get(auth_token=uuid_token)
    except NotificationBot.DoesNotExist:
        return None


@sync_to_async
def get_from_notifbot_by_chat_id(chat_id):
    """
    Asynchronous data retrieval from model NotificationBot by chat_id
    """
    try:
        return NotificationBot.objects.get(telegram_chat_id=chat_id)
    except NotificationBot.DoesNotExist:
        return None

@sync_to_async
def get_from_tasks_to_complete_by_user_id(user_id):
    """
    Asynchronous data retrieval from model TasksToComplete by user_id.
    In param user_id from model NotificationBot.
    """
    try:
        return list(TaskToComplete.objects.filter(user_id=user_id))
    except TaskToComplete.DoesNotExist:
        return None

@sync_to_async
def get_from_tasks_to_complete_by_task_id(task_id):
    """
    Asynchronous data retrieval from model TaskToComplete by task_id.
    """
    try:
        return TaskToComplete.objects.get(id=task_id)
    except TaskToComplete.DoesNotExist:
        return None

@sync_to_async
def turn_off_notification_setting(user_id):
    """
    Asynchronous data update of notif time and deadline into Null.
    In param user_id from model NotificationBot.
    """
    return TaskToComplete.objects.filter(user_id=user_id).update(notification_time=None, task_deadline = None)

@sync_to_async
def get_notification_time(user_id):
    """
    Asynchronous data retrieval of notification_time from model TasksToComplete by user_id.
    In param user_id from model NotificationBot.
    """
    try:
        notif_time = TaskToComplete.objects.get(user_id=user_id).notification_time

        if notif_time is None:
            return None

        if notif_time.tzinfo is None:
            notif_time = notif_time.replace(tzinfo=ZoneInfo("Europe/Kyiv"))

        return notif_time
    except TaskToComplete.DoesNotExist:
        return None

@sync_to_async
def save_complete_to_completed(task_text, time, user_id):
    """
    Asynchronous save task to complete to CompletedTasks
    :param task_text: TasksToComplete object.task_text
    :param time: timezone.now()
    :param user_id: TasksToComplete object.user_id
    :return:
    """
    CompletedTask.objects.create(
        task_text=task_text,
        task_complete=time,
        user_id=user_id
    )

@sync_to_async
def save_to_db(data):
    """
    Asynchronous data storage in db
    """
    data.save()

@sync_to_async
def delete_task(task):
    """
    asynchronous task deletion
    """
    task.delete()