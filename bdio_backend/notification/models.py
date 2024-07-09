from django.db import models
from user.models import User

class Notification(models.Model):
    user = models.ManyToManyField(User)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)