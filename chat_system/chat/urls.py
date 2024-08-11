from django.urls import path
from . import views

urlpatterns = [
    path('chat-rooms/', views.get_chat_rooms, name='get_chat_rooms'), 
    path('chat-rooms/<int:chat_room_id>/', views.get_chat_room_detail, name='get_chat_room_detail'),  
    path('chat-rooms/<int:chat_room_id>/users/', views.get_all_users_in_chat_room, name='get_all_users_in_chat_room'), 
    path('chat-rooms/<int:chat_room_id>/messages/', views.get_chat_room_message, name='get_chat_room_message'),
    path('chat-rooms/', views.create_chat_room, name='create_chat_room'), 
    path('chat-rooms/bulk-add-users/', views.bulk_add_users_to_chat_room, name='bulk_add_users_to_chat_room'), 
    path('chat-rooms/<int:chat_room_id>/user/join/', views.add_user_to_chat_room, name='add_user_to_chat_room'), 
    path('chat-rooms/<int:chat_room_id>/user/delete/', views.delete_user_from_chat_room, name='delete_user_from_chat_room'),  
    path('chat-rooms/<int:chat_room_id>/delete/', views.delete_chat_room, name='delete_chat_room'), 
    path('users/<int:user_id>/chat-rooms/', views.get_chat_room_by_user, name='get_chat_rooms_by_user'), 
]
