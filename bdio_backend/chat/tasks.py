from celery import shared_task
from chat.models import Conversation, ConversationMessage
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from django.utils import timezone
from django.conf import settings
from core.utils import get_profile_image_with_ouath2

@shared_task
def send_update_chat_to_channel_task(conversation_id: str):
    
    conversation = Conversation.objects.get(id=conversation_id)
    users = conversation.users.all()
    channel_layer = get_channel_layer()
    
    last_message = ConversationMessage.objects.filter(conversation=conversation.id).order_by('-created_at').first()
    message_created_by = last_message.created_by
    users_dict = [{
            "id": str(user.id),
            "first_name": user.first_name,
            "last_name": user.last_name,
            "profile_image": get_profile_image_with_ouath2(user)
        } for user in users]
    
    if last_message is None:
        last_message_dict = None
    else:
        last_message_dict = {
        "id": str(last_message.id),
        "conversation": str(conversation.id),
        "body": last_message.body,
        "created_at": last_message.created_at.astimezone(timezone.get_current_timezone()).strftime('%Y-%m-%dT%H:%M:%S.%f%z'),
        "created_by": {
            "id": str(message_created_by.id),
            "first_name": message_created_by.first_name,
            "last_name": message_created_by.last_name,
            "profile_image": get_profile_image_with_ouath2(message_created_by),
            },
        "file": f"{settings.BACKEND_URL}{last_message.file.url}" if last_message.file else None
        }

    conversation_id = str(conversation.id)
    created_at = conversation.created_at.astimezone(timezone.get_current_timezone()).strftime('%Y-%m-%dT%H:%M:%S.%f%z')
    created_by_id = str(conversation.created_by.id)
    updated_at = conversation.updated_at.astimezone(timezone.get_current_timezone()).strftime('%Y-%m-%dT%H:%M:%S.%f%z')
    
    for user in users:
        
        async_to_sync(channel_layer.group_send)(
            f'user_chat_list_{str(user.id)}',
            {
                "type": "send_updated_chat",
                "id": conversation_id,
                "last_message": last_message_dict,
                "created_at": created_at,
                "updated_at": updated_at,
                "users": users_dict,
                "created_by": created_by_id
            }
        )