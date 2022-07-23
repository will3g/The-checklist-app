from django.db import models
from django.conf import settings

from datetime import datetime

UserProfile = settings.AUTH_USER_MODEL

class Task(models.Model):
    author = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    title = models.CharField(max_length=500, blank=True)
    description = models.TextField(blank=True)
    thumbnail = models.ImageField(upload_to='fotos/%d/%m/%Y', blank=True)
    primary_color = models.CharField(max_length=30)
    secondary_color = models.CharField(max_length=30)
    subtasks = models.JSONField()
    created_at = models.DateTimeField(
        default=datetime.now,
        blank=True
    )

    def __str__(self):
        return self.title
