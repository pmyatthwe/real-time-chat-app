from rest_framework import serializers
from django.conf import settings
from .models import ChatRoom, Message, UserChatRoom
from users.serializers import UserSerializer


class ChatRoomSerializer(serializers.ModelSerializer):
    online_count = serializers.SerializerMethodField()
    online_users = serializers.SerializerMethodField()

    class Meta:
        model = ChatRoom
        fields = ('id', 'name', 'created_at', 'online_count', 'online_users')

    def get_online_count(self, obj):
        return obj.get_online_count()
    
    def get_online_users(self, obj):
        return [user.id for user in obj.online.all()]


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