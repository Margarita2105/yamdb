from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    user = 'user'
    moderator = 'moderator'
    admin = 'admin'

    rank=[
        ('user', 'user'),
        ('moderator', 'moderator'),
        ('admin', 'admin'),
    ]
    password = models.CharField(max_length=9, blank=True, null=True)
    role = models.CharField(max_length=9, choices=rank, default=user)
    bio = models.CharField(max_length=255, blank=True, null=True)
    email = models.EmailField(unique=True)
