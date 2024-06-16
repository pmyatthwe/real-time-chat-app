from rest_framework import serializers
from django.conf import settings
from .models import ChatRoom, Message, UserChatRoom
from users.serializers import UserSerializer


class ChatRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatRoom
        fields = ('id', 'name', 'created_at')


class MessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)
    chat_room = ChatRoomSerializer(read_only=True)

    class Meta:
        model = Message
        fields = '__all__'


class UserChatRoomSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    chat_room = ChatRoomSerializer(read_only=True)
    
    class Meta:
        model = UserChatRoom
        fields = '__all__'