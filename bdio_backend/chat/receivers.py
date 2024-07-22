from django.db.models.signals import post_save
from django.dispatch import receiver
from chat.models import Conversation, ConversationMessage
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from django.utils import timezone
from django.conf import settings
from core.utils import get_profile_image_with_ouath2
from chat.tasks import send_update_chat_to_channel_task

@receiver(post_save, sender=ConversationMessage)
def send_update_chat_to_channel(sender, instance, created, **kwargs):
    if created:
        send_update_chat_to_channel_task.delay(str(instance.conversation.id))
