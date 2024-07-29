from django.db.models.signals import post_save
from django.dispatch import receiver
from chat.models import Conversation, ConversationMessage
from chat.tasks import send_update_chat_to_channel_task, send_message_task

@receiver(post_save, sender=ConversationMessage)
def send_update_chat_to_channel(sender, instance, created, **kwargs):
    if created:
        send_update_chat_to_channel_task.delay(str(instance.conversation.id), str(instance.created_by.id))
        
@receiver(post_save, sender=ConversationMessage)
def send_message(sender, instance, created, **kwargs):
    if created:
        send_message_task(str(instance.id), f"chat_{instance.conversation.id}")