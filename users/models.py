from django.db import models

from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    storage_path = models.CharField()

class AuthToken(models.Model):
    token = models.CharField(max_length=128)