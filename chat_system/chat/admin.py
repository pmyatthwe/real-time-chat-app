from django.contrib import admin
from .models import ChatRoom, UserChatRoom, Message

admin.site.register(ChatRoom)
admin.site.register(UserChatRoom)
admin.site.register(Message)