from django.urls import path
from . import views

urlpatterns = [
    path('create-chat/', views.create_chat_room),
    path('add-chat-room/', views.add_user_to_chat_room),
    path('messages/<int:room_id>', views.get_chat_room_message)
]
