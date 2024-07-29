from django.db.models.signals import post_save
from django.dispatch import receiver
from notification.models import UserNotification
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

@receiver(post_save, sender=UserNotification)
def send_update_chat_to_channel(sender, instance, created, **kwargs):
    user = instance.user
    count = UserNotification.objects.filter(user=user, is_read=False).count()
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        f'notifications_{user.id}',
        {
            'type': 'get_unread_notification_count',
            'unread_notification_count': count
        }
    )
