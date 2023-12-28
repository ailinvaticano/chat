import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import Message


class ChatConsumer(AsyncWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.room_name = None
        self.room_group_name = None

    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_id']
        self.room_group_name = f'chat_{self.room_name}'

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name,
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name,
        )

        # Receive message from WebSocket

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['content']
        author = self.scope["user"].username

        # Save message to the database
        Message.objects.create(room_id=self.room_name, sender=self.scope["user"], content=message)

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat.message',
                'author': author,
                'content': message,
            }
        )

        # Receive message from room group

    async def chat_message(self, event):
        author = event['author']
        message = event['content']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'author': author,
            'content': message,
        }))

    async def send_group_message(self, content, room_id):
        # Broadcast the message to all clients in the same group (chat room)
        await self.channel_layer.group_send(
            f'chat_{room_id}',
            {
                'type': 'chat.message',
                'content': content,
            }
        )

