import json
from django.utils import timezone
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
from chat.models import ConversationMessage, Conversation
from user.models import User
from django.conf import settings
from channels.db import database_sync_to_async


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope['user']
        
        if not self.user.is_authenticated:
            await self.close()
            
        self.conversation_id = str(self.scope['url_route']['kwargs']['conversation_id'])
        self.conversation_group_name = f'chat_{self.conversation_id}'
        
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
        user = self.scope['user']
        try:
            data = json.loads(text_data)
            body = data['data']['body']
            
            conversation = await database_sync_to_async(Conversation.objects.get)(id=self.conversation_id)
            
            await database_sync_to_async(ConversationMessage.objects.create)(
                conversation=conversation,
                body=body,
                created_by=user
            )
        except json.JSONDecodeError:
            print("Error decoding JSON")
        except Conversation.DoesNotExist:
            print("Conversation does not exist")
        except Exception as e:
            print(f"An error occurred: {e}")


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


class ChatListConsumer(AsyncWebsocketConsumer):
    """
    Represents a consumer for handling new updated chat functionality.

    This consumer handles WebSocket connections for retrieving in real-time newest updated chat to add to chat list.
    """

    async def connect(self):
        """
        Called when the WebSocket is handshaking as part of the connection process.

        This method adds the consumer to the personal notification group and accepts the connection.
        """
        self.user = self.scope['user']
        
        if self.user.is_authenticated:
            self.personal_group_name = f'user_chat_list_{self.user.id}'

            await self.channel_layer.group_add(
                self.personal_group_name,
                self.channel_name
            )

            await self.accept()
        else:
            await self.close()

    async def disconnect(self, close_code):
        """
        Called when the WebSocket closes for any reason.

        This method removes the consumer from the personal notification group.
        """
        await self.channel_layer.group_discard(
            self.personal_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        """
        Called when a WebSocket frame is received.

        This method is currently empty and can be implemented to handle received WebSocket frames.
        """
        pass

    async def send_updated_chat(self, event):
        """
        Sends the updated chat list to the connected WebSocket client.

        This method retrieves the updated chat list and sends it to the client as a JSON string.
        """
        await self.send(text_data=json.dumps({
            'id': event['id'],
            'last_message': event['last_message'],
            'created_at': event['created_at'],
            'updated_at': event['updated_at'],
            'users': event['users'],
            'created_by': event['created_by']
        }))