from celery import shared_task
from notification.models import Notification, UserNotification
from user.models import User
from django.db.models import QuerySet
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from django.utils import timezone

@shared_task
def send_notification_task(user_ids, message):
    
    channel_layer = get_channel_layer()
    notification = Notification.objects.create(message=message)
    
    for user_id in user_ids:
        user = User.objects.get(id=user_id)
        notification_user = UserNotification.objects.create(user=user, notification=notification)
        
        async_to_sync(channel_layer.group_send)(
            f'notifications_{user.id}',
            {
                'type': 'send_notification',
                'id': notification_user.notification.id,
                'notification': {'message': notification_user.notification.message},
                'created_at': notification_user.created_at.astimezone(timezone.get_current_timezone()).strftime('%Y-%m-%dT%H:%M:%S.%f%z'),
                'is_read': notification_user.is_read
            }
        )