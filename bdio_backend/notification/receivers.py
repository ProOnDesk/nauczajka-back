from django.db.models.signals import post_save
from django.dispatch import receiver
from notification.utils import send_unread_notification_count_to_channel, send_notification
from notification.models import UserNotification, UserChatNotification, Notification
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from user.models import User


@receiver(post_save, sender=UserNotification)
def send_unread_notification(sender, instance, created, **kwargs):
    send_unread_notification_count_to_channel(instance.user)
    
    if created:
        send_notification(user_id=str(instance.user.id), notification_id=str(instance.notification.id))
    
@receiver(post_save, sender=User)
def create_user_chat_notification(sender, instance, created, **kwargs):
    if created:
        notification = Notification.objects.create(message="")
        user_notification = UserNotification.objects.create(user=instance, notification=notification)
        UserChatNotification.objects.create(user_notification=user_notification, user=instance)
        user_notification.save()