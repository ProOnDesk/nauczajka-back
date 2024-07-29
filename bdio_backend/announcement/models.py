from django.db import models
from tutor.models import Tutor

class Tag(models.Model):
    name = models.CharField(max_length=100, unique=True, primary_key=True)

class Announcement(models.Model):
    id = models.AutoField(unique=True)
    title = models.CharField(max_length=200)
    description = models.TextField()
    tutor = models.ForeignKey(Tutor, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    tags = models.ManyToManyField(Tag)

