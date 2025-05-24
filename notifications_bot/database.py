from asgiref.sync import sync_to_async


def django_db_setup():
    import os
    import django
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'todo.settings')
    django.setup()


django_db_setup()
from cabinet.models import NotificationBot



@sync_to_async
def get_from_db_by_token(uuid_token):
    """
    Asynchronous data retrieval from db by uuid_token
    """
    try:
        return NotificationBot.objects.get(auth_token=uuid_token)
    except NotificationBot.DoesNotExist:
        return None


@sync_to_async
def get_from_db_by_chat_id(chat_id):
    """
    Asynchronous data retrieval from db by chat_id
    """
    try:
        return NotificationBot.objects.get(telegram_chat_id=chat_id)
    except NotificationBot.DoesNotExist:
        return None

@sync_to_async
def save_to_db(data):
    """
    Asynchronous data storage in db
    """
    data.save()
