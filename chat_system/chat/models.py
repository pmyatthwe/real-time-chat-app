from django.db import models
from users.models import User
from django.utils.translation import gettext_lazy as _


class ChatRoom(models.Model):
    name = models.CharField(max_length=32)
    created_at = models.DateTimeField(auto_now_add=True)


class Message(models.Model):
    class MessageType(models.TextChoices):
        TEXT = 'TXT', _('Text')
        IMAGE = 'IMG', _('Image')

    sender_id = models.ForeignKey(User, on_delete=models.SET_NULL)
    chat_room_id = models.ForeignKey(ChatRoom, on_delete=models.CASCADE)
    content = models.CharField(max_length=255, null=True, blank=True)
    message_type = models.CharField(max_length=3, choices=MessageType.choices, default=MessageType.TEXT)
    timestamp = models.DateTimeField(auto_now_add=True)
    seen = models.BooleanField(default=False)


class UserChatRoom(models.Model):
    chat_room_id = models.ForeignKey(ChatRoom, on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)


#https://bytebytego.com/courses/system-design-interview/design-a-chat-system