from django.db import models
from user.models import User

class Notification(models.Model):
    users = models.ManyToManyField(User, related_name='notifications')
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
