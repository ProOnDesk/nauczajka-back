import json
from channels.generic.websocket import AsyncWebsocketConsumer
from django.utils import timezone
from asgiref.sync import sync_to_async
from notification.models import Notification
from notification.utils import send_unread_notification_count_to_channel

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
        
        if not self.user.is_authenticated:
            await self.close()
        
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
        try:
            data = json.loads(text_data)
            send_back = data['data']['send_back_unread_notification_count']
            if send_back:
                await sync_to_async(send_unread_notification_count_to_channel)(self.user)
            
        except json.JSONDecodeError:
            print("Error decoding JSON")
        except Exception as e:
            print(f"An error occurred: {e}")

    
    async def send_notification(self, event):
        """
        Sends a notification to the connected WebSocket client.

        This method is called by the channel layer when a notification needs to be sent.
        It sends the notification message to the connected client.
        """
        await self.send(text_data=json.dumps({
            'id': event['id'],
            'notification': event['notification'],
            'created_at': event['created_at'],
            'is_read': event['is_read']
        }))
        
    async def get_unread_notification_count(self, event):
        """
        Sends the number of unread notifications to the connected WebSocket client.

        This method is called by the channel layer when the number of unread notifications
        needs to be sent. It sends the number of unread notifications to the connected client.
        """
        await self.send(text_data=json.dumps({
            'unread_notification_count': event['unread_notification_count']
        }))