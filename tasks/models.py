from django.db import models


class TaskToComplete(models.Model):
    task_text = models.TextField()
    task_deadline = models.DateTimeField(null=True, blank=True)
    notification_time = models.DateTimeField(null=True, blank=True)
    user = models.ForeignKey(
        'registration.Users',
        on_delete=models.CASCADE,
        db_column='user_id',
    )

    class Meta:
        db_table = 'tasks_to_complete'


class CompletedTask(models.Model):
    task_text = models.TextField()
    task_complete = models.DateTimeField()
    user = models.ForeignKey(
        'registration.Users',
        on_delete=models.CASCADE,
        db_column='user_id',
    )

    class Meta:
        db_table = 'completed_tasks'