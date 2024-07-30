from notification.tasks import send_notification_task
from notification.models import Notification, UserNotification
from user.models import User
from django.db.models import QuerySet
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from django.utils import timezone

def send_notification(users, message):
    
    if isinstance(users, User):
        users = [users]
        
    elif isinstance(users, QuerySet):
        users = list(users)
    else:
        return False
        
    user_ids = [str(user.id) for user in users]

    send_notification_task.delay(user_ids, message)

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