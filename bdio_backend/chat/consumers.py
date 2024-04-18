import json

from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async

from .models import Conversation, ConversationMessage


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.conversation_id = self.scope['url_route']['kwargs']['conversation_id']
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
        
        # Recieve message from web sockets
    async def receive(self, text_data):
        data = json.loads(text_data)

        username = data['data']['username']
        body = data['data']['body']
        created_by = data['data']['created_by']

        message = await self.save_message(self.conversation_id, body, username)

        
        await self.channel_layer.group_send(
            self.conversation_group_name,
            {
                'type': 'chat_message',
                'body': body,
                'username': username,
                'created_by': created_by,
                'message_id': self.last_message_id
            }
        )

    
    # Sending messages
    async def chat_message(self, event):
        body = event['body']
        created_by = event['created_by']
        username = event['username']

        await self.send(text_data=json.dumps({
            'body': body,
            'username': username,
            'created_by': created_by,
            'message_id': self.last_message_id,
        }))

    @sync_to_async
    def save_message(self, conversation_id, body, username):
        user = self.scope['user']

        conversation = ConversationMessage.objects.create(conversation_id=conversation_id, body=body, created_by=user, username=username)
        self.last_message_id = str(conversation.id)
 