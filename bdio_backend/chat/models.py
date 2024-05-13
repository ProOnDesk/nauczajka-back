from django.db import models
from user.models import User
import uuid

class Conversation(models.Model):
    """
    Conversation model
    """
    id = models.UUIDField(primary_key=True, editable=False, unique=True, default=uuid.uuid4)
    users = models.ManyToManyField(User, related_name='conversations')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        users_emails = " ".join(f'{user.email}, ' for user in self.users.all())
        return f'{self.id} - {users_emails}'
    
class ConversationMessage(models.Model):
    """
    Conversation message model
    """
    id = models.UUIDField(primary_key=True, editable=False, unique=True, default=uuid.uuid4)
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='messages')
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='messages')
