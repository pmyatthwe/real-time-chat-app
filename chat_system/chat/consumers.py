import json
from asgiref.sync import sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from rest_framework import status
from rest_framework.response import Response
from .models import ChatRoom, Message
from users.models import User
from .enums import JwtError


class ChatConsumer(AsyncWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.room_name = None
        self.room_group_name = None
        self.room = None
        self.user = None
        
    async def connect(self):
        """
        This function works on the websocket instance which has been created and 
        when the connection is open or created, it connects and accepts the connection. 
        It creates a group name for the chatroom and adds the group to the channel 
        layer group. 
        """
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'chat_{self.room_name}'
        self.room = await sync_to_async(ChatRoom.objects.get)(name=self.room_name)

        if self.scope['error'] == JwtError.INVALID:
            return Response({"message": "Invalid token."}, status=status.HTTP_401_UNAUTHORIZED)
        
        if self.scope['error'] == JwtError.NO_TOKEN:
            return Response({"message": "No token provided."}, status=status.HTTP_400_BAD_REQUEST)
        
        self.user = self.scope['user_id']
        self.user = await sync_to_async(User.objects.get)(id=self.user)

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()
        await sync_to_async(self.room.join_chat)(self.user)


    async def disconnect(self, close_code):
        """
        This just removes the instance from the group. 
        """
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
        await sync_to_async(self.room.leave_chat)(self.user)

    async def receive(self, text_data):
        """
        Send message to room group
        """
        data = json.loads(text_data)
        message = data['message']

        await sync_to_async(Message.objects.create)(
            sender=self.user,
            chat_room=self.room,
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
        await self.send(text_data=json.dumps(event))
