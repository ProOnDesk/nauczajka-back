from notification.tasks import send_notification_task
from notification.models import Notification, UserNotification
from chat.models import ConversationReadStatus
from user.models import User
from django.db.models import QuerySet
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from django.utils import timezone
from typing import Union

def send_notification(user_id: str, notification_id: str):
    send_notification_task.delay(user_id, notification_id)

def send_unread_notification_count_to_channel(user):
    count = UserNotification.objects.filter(user=user, is_read=False).count()
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        f'notifications_{user.id}',
        {
            'type': 'get_unread_notification_count',
            'unread_notification_count': count
        }
    )