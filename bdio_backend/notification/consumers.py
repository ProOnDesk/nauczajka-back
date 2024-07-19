import json
from channels.generic.websocket import AsyncWebsocketConsumer
from django.utils import timezone
from asgiref.sync import sync_to_async
from notification.models import Notification


class NotificationConsumer(AsyncWebsocketConsumer):
    """
    WebSocket consumer for handling notifications.

    This consumer handles the connection, disconnection, and receiving of messages
    from clients. It also sends notifications to the appropriate groups based on
    the received data.

    Attributes:
        user (User): The user associated with the WebSocket connection.
        general_group_name (str): The name of the general notification group.
        personal_group_name (str): The name of the personal notification group.
    """

    async def connect(self):
        """
        Called when the WebSocket is handshaking as part of the connection process.

        This method adds the consumer to the general and personal notification groups
        and accepts the connection.
        """
        self.user = self.scope['user']
        self.personal_group_name = f'notifications_{self.user.id}'

        await self.channel_layer.group_add(
            self.personal_group_name,
            self.channel_name
        )

        await self.accept()
        
    async def disconnect(self, close_node):
        """
        Called when the WebSocket closes for any reason.

        This method removes the consumer from the general and personal notification groups.
        """
        
        await self.channel_layer.group_discard(
            self.personal_group_name,
            self.channel_name
        )
        
    async def receive(self, text_data):
        """
        Called when a WebSocket frame is received.
        
        No logic is needed here because notifications are directly handled 
        using Django's get_channel_layer and are sent directly if needed, 
        without using WebSockets directly.
        """
        
        pass
    
    async def send_notification(self, event):
        """
        Sends a notification to the connected WebSocket client.

        This method is called by the channel layer when a notification needs to be sent.
        It sends the notification message to the connected client.
        """
        await self.send(text_data=json.dumps({
            'message': event['message']
        }))
        