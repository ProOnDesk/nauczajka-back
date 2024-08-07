from django.db import models
from tutor.models import Tutor

class Tag(models.Model):
    name = models.CharField(max_length=100, unique=True, primary_key=True)

    def __str__(self):
        return f'Tag name - "{self.name}"'
    
    
class Announcement(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200)
    description = models.TextField()
    tutor = models.ForeignKey(Tutor, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    tags = models.ManyToManyField(Tag, related_name='announcements')

    def __str__(self):
        return f'Title - "{self.title}" by {self.tutor.user.email}'
