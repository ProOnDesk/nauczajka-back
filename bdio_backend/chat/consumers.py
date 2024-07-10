import json
from django.utils import timezone
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
from .models import ConversationMessage
from user.models import User
from django.conf import settings
from rest_framework.serializers import DateTimeField

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.conversation_id = str(self.scope['url_route']['kwargs']['conversation_id'])
        self.conversation_group_name = f'chat_{self.conversation_id}'

        # Join conversation group
        await self.channel_layer.group_add(
            self.conversation_group_name,
            self.channel_name
        )

        await self.accept()
        
    async def disconnect(self, close_code):
        # Leave conversation group
        await self.channel_layer.group_discard(
            self.conversation_group_name,
            self.channel_name
        )
        
    async def receive(self, text_data):
        data = json.loads(text_data)

        body = data['data']['body']
        user = self.scope['user']

        message = await self.save_message(self.conversation_id, body, user)
        created_at_formatted = message.created_at.astimezone(timezone.get_current_timezone()).strftime('%Y-%m-%dT%H:%M:%S.%f%z')
        
        
        await self.channel_layer.group_send(
            self.conversation_group_name,
            {
                'type': 'chat_message',
                'id': str(message.id),
                'conversation': self.conversation_id,
                'body': message.body,
                'created_at': created_at_formatted,
                'file': message.file.name,     
                'created_by': {
                    'id': str(user.id),
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                    'profile_image': f"{user.profile_image.url}",
                }
            }
        )

    async def chat_message(self, event):
        id = event['id']
        conversation = event['conversation']
        body = event['body']
        created_at = event['created_at']
        created_by = event['created_by']
        file = event['file']

        await self.send(text_data=json.dumps({
            'id': str(id),
            'conversation': conversation,
            'body': body,
            'file': file,
            'created_at': created_at,
            'created_by': created_by,
        }))

    @sync_to_async
    def save_message(self, conversation_id, body, created_by):
        message = ConversationMessage.objects.create(conversation_id=conversation_id, body=body, created_by=created_by)
        self.last_message = message
        
        return message
