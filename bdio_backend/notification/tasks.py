from celery import shared_task
from notification.utils import (
    send_general_notification,
    send_personal_notification
)
from user.models import User

@shared_task
def send_personal_notification_task(user_id, message):
    users = User.objects.filter(id__in=user_id)
    send_personal_notification(users, message)

@shared_task
def send_general_notification_task(message):
    send_general_notification(message=message)