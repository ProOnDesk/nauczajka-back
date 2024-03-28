from django.db import models
from user.models import User

# Create your models here.
class Tutor(models.Model):
    """
    Tutor model
    """
    user = models.OneToOneField(User, primary_key=True, on_delete=models.CASCADE)
    description = models.TextField()
    
    def __str__(self):
        return f"Tutor - {self.user.email}"
    