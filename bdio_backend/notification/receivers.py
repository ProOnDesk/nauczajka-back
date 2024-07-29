from django.db.models.signals import post_save
from django.dispatch import receiver
from notification.utils import send_unread_notification_count_to_channel
from notification.models import UserNotification
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

@receiver(post_save, sender=UserNotification)
def send_unread_notification(sender, instance, created, **kwargs):
    send_unread_notification_count_to_channel(instance.user)

