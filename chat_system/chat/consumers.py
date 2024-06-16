import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import ChatRoom, Message
from users.models import User
from asgiref.sync import sync_to_async


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        """
        This function works on the websocket instance which has been created and 
        when the connection is open or created, it connects and accepts the connection. 
        It creates a group name for the chatroom and adds the group to the channel 
        layer group. 
        """
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'chat_{self.room_name}'

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        """
        This just removes the instance from the group. 
        """
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        """
        Send message to room group
        """
        data = json.loads(text_data)
        room_id = data['room_id']
        sender_id = data['sender_id']
        message = data['message']

        sender = await sync_to_async(User.objects.get)(id=sender_id)
        room = await sync_to_async(ChatRoom.objects.get)(id=room_id)

        new_message = await sync_to_async(Message.objects.create)(
            sender=sender,
            chat_room=room,
            content=message,
            message_type="TXT"
        )

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
            }
        )

    async def chat_message(self, event):
        """
        Send message to WebSocket
        """
        message = event['message']

        await self.send(text_data=json.dumps({
            'message': message,
        }))
