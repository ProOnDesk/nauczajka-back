from django.db import models
from user.models import User
import uuid
from os import path as os_path

def get_upload_conversation_message_file_path(instance, filename):
    return os_path.join('uploads', 'chat', 'message', f'{instance.id}', filename)


class Conversation(models.Model):
    """
    Conversation model
    """
    id = models.UUIDField(primary_key=True, editable=False, unique=True, default=uuid.uuid4)
    users = models.ManyToManyField(User, related_name='conversations')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_by_conversations')
    
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
    file = models.FileField(upload_to=get_upload_conversation_message_file_path, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='messages')
    
    def __str__(self):
        return f'ID message: {self.id} from ID conversation: {self.conversation}'


class ConversationReadStatus(models.Model):
    """
    Model to track read status of conversations for each user
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='read_statuses')
    is_read = models.BooleanField(default=False)
    read_at = models.DateTimeField(null=True, blank=True)
    is_connected_to_chat = models.BooleanField(default=False)

    class Meta:
        unique_together = ('user', 'conversation')
    
    def __str__(self):
        return f'User: {self.user.email} - Conversation ID: {self.conversation.id} - Read: {self.is_read}'