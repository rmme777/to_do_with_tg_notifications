# Generated by Django 5.2.1 on 2025-05-23 16:43

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cabinet', '0002_notificationbot_auth_token_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notificationbot',
            name='auth_token',
            field=models.UUIDField(default=uuid.uuid4, editable=False, unique=True),
        ),
        migrations.AlterField(
            model_name='notificationbot',
            name='notifications_included',
            field=models.BooleanField(blank=True, null=True),
        ),
    ]
