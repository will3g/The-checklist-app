from django.db import models
from django.contrib.auth.models import AbstractUser


class UserProfile(AbstractUser):
    thumbnail = models.ImageField(upload_to='fotos/%d/%m/%Y', blank=True)
    profile_color = models.CharField(max_length=30)

    def __str__(self):
        return self.username
