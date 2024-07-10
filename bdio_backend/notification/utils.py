from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from notification.models import Notification
from user.models import User

def send_general_notification(message):
    channel_layer = get_channel_layer()
    
    notification = Notification.objects.create(message=message)
    
    for user in User.objects.filter(is_confirmed=True):
        notification.users.add(user)
        
    async_to_sync(channel_layer.group_send)(
        'notifications',
        {
            'type': 'send_notification',
            'message': message,
        }
    )
    
def send_personal_notification(users, message):
    channel_layer = get_channel_layer()
    
    notification = Notification.objects.create(message=message)
    if isinstance(users, User):
        notification.users.add(users)
        async_to_sync(channel_layer.group_send)(
            f'notifications_{users.id}',
            {
                'type': 'send_notification',
                'message': message,
            }
        )
    else:
        for user in users:
            notification.users.add(user)
            async_to_sync(channel_layer.group_send)(
                f'notifications_{user.id}',
                {
                    'type': 'send_notification',
                    'message': message,
                }
            )