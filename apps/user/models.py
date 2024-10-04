from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.db import models
from .managers import UserManager


class User(AbstractUser, PermissionsMixin):
    followers = models.ManyToManyField('self', symmetrical=False, related_name='following', blank=True)

    objects = UserManager() 

    def __str__(self):
        return self.username
