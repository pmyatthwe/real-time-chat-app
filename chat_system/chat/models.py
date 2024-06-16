from django.db import models
from users.models import User
from django.utils.translation import gettext_lazy as _


class ChatRoom(models.Model):
    # owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owner')
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Message(models.Model):
    class MessageType(models.TextChoices):
        TEXT = 'TXT', _('Text')
        IMAGE = 'IMG', _('Image')

    sender = models.ForeignKey(User, null=True, on_delete=models.SET_NULL, related_name='sender_messages')
    chat_room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE, related_name='chat_room_messages')
    content = models.CharField(max_length=255, null=True, blank=True)
    message_type = models.CharField(max_length=3, choices=MessageType.choices, default=MessageType.TEXT)
    timestamp = models.DateTimeField(auto_now_add=True)
    seen = models.BooleanField(default=False)

    class Meta:
        ordering = ['timestamp']

    def __str__(self):
        return f"{self.sender}: {self.message_type}"


class UserChatRoom(models.Model):
    chat_room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE, related_name='chat_room')
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL, related_name='user_chat_room')

    class Meta:
        unique_together = ('chat_room', 'user')

    def __str__(self):
        return f"{self.user} in {self.chat_room}"
