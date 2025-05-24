from django.db import models
from uuid import uuid4

class NotificationBot(models.Model):
    user = models.ForeignKey(
            'registration.Users',
             on_delete=models.CASCADE,
             db_column='user_id',
    )
    authorized = models.BooleanField(default=False)
    notifications_included = models.BooleanField(null=True, blank=True)
    telegram_chat_id = models.BigIntegerField(null=True, blank=True)
    auth_token = models.UUIDField(default=uuid4, editable=False, unique=True)

    class Meta:
        db_table = 'notification_bot'


