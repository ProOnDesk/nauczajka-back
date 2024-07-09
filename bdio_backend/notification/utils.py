from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

def send_general_notification(message):
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        'notifications_general',
        {
            'type': 'send_notification',
            'message': message,
        }
    )
    
def send_personal_notification(user, message):
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        f'notifications_{user.id}',
        {
            'type': 'send_notification',
            'message': message,
        }
    )