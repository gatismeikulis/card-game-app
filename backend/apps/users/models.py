from typing import override
from django.db.models import CharField, TextField
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    # AbstractUser already has fields:
    # username, password, email, first_name, last_name, is_staff, is_active, is_superuser, last_login, date_joined
    screen_name = CharField(max_length=100, unique=True)
    description = TextField(blank=True)

    @override
    def __str__(self):
        return f"{self.username} [{self.pk}] ({self.screen_name})"
