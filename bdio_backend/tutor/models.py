from django.db import models
from user.models import User

class Tutor(models.Model):
    """
    Tutor model
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    description = models.TextField()
    skills = models.ManyToManyField('Skills', related_name='tutors')
    
    def __str__(self):
        return f"Tutor - {self.user.email}"
    

class Skills(models.Model):
    """
    Skills model
    """
    skill = models.CharField(max_length=100, primary_key=True, unique=True)

    def __str__(self):
        return f"Skill - {self.skill}"