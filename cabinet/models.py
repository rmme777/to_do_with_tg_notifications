from django.db import models


class NotificationBot(models.Model):
    user = models.ForeignKey(
            'registration.Users',
             on_delete=models.CASCADE,
             db_column='user_id',
    )
    authorized = models.BooleanField(default=False)
    notifications_included = models.BooleanField(default=True)
    notification_time = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'notification_bot'


