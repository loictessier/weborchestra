from django.db import models
from django.contrib.auth.models import AbstractUser


class Profile(AbstractUser):
    signup_confirmation = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Profil'

    def __str__(self):
        return self.username
