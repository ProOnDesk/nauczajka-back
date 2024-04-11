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
    
class ConversationMessage(models.Model):
    """
    Conversation message model
    """
    id = models.UUIDField(primary_key=True, editable=False, unique=True, default=uuid.uuid4)
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='messages')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='messages')