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
