import json
from channels.generic.websocket import AsyncWebsocketConsumer
from django.utils import timezone
from channels.db import database_sync_to_async

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'chat_{self.room_name}'
        
        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json.get('message', '')
        sender_name = text_data_json.get('sender_name', '')
        receiver_name = text_data_json.get('receiver_name', '')
        
        if message and sender_name and receiver_name:
            # Save message to database
            await self.save_message(sender_name, receiver_name, message)
            
            # Send message to room group
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message': message,
                    'sender': sender_name
                }
            )

    # Receive message from room group
    async def chat_message(self, event):
        message = event['message']
        sender = event['sender']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'type': 'chat_message',
            'message': message,
            'sender': sender
        }))

    @database_sync_to_async
    def save_message(self, sender_name, receiver_name, message):
        from django.contrib.auth.models import User
        from chat.models import Messages
        
        sender = User.objects.get(username=sender_name)
        receiver = User.objects.get(username=receiver_name)

        new_message = Messages(
            description=message,
            sender_name=sender,
            receiver_name=receiver,
            time=timezone.now().time(),
            timestamp=timezone.now(),
            seen=False
        )
        new_message.save()