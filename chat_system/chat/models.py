from django.db import models
from users.models import User
from django.utils.translation import gettext_lazy as _


class ChatRoom(models.Model):
    name = models.CharField(max_length=100)
    online = models.ManyToManyField(to=User, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
    def get_online_count(self):
        return self.online.count()
    
    def join_chat(self, user):
        self.online.add(user)
        self.save()

    def leave_chat(self, user):
        self.online.remove(user)
        self.save()


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
