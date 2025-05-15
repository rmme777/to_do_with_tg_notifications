from django.contrib.auth.models import AbstractUser
from django.db import models

class Users(AbstractUser):
    username = None
    login = models.EmailField(unique=True)

    USERNAME_FIELD = 'login'
    REQUIRED_FIELDS = []

    class Meta:
        db_table = 'users'

