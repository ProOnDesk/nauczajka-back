from channels.generic.websocket import AsyncWebsocketConsumer


class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope['user']
        
        self.general_group_name = 'notifications'
        self.personal_group_name = f'notifactions_{user.id}'
        
        await self.channel_layer.group_add(
            self.general_group_name,
            self.channel_name
        )
        
        await self.channel_layer.group_add(
            self.personal_group_name,
            self.channel_name
        )
        
        await self.accept()
        
    async def disconnect(self, close_node):
        await self.channel_layer.group_discard(
            self.general_group_name,
            self.channel_name
        )
        
        await self.channel_layer.group_discard(
            self.personal_group_name,
            self.channel_name
        )
        
    async def receive(self, text_data):
        pass
    
    async def send_notification(self, event):
        await self.send(text_data=json.dumps({
            'message': event['message']
        }))        
