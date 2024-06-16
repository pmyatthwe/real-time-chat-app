from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .models import ChatRoom, UserChatRoom, Message
from users.models import User
from .serializers import MessageSerializer


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_chat_room(request):
    room_name = request.data.get("room_name")
    if not room_name:
        return Response({"message", "room name is required."},status=status.HTTP_400_BAD_REQUEST)
    
    chat_room, _ = ChatRoom.objects.get_or_create(
        name=room_name
    )
    return Response({'room_name': chat_room.id}, status=status.HTTP_201_CREATED)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_user_to_chat_room(request):
    room_id = request.data.get("room_id")
    user_id = request.data.get("user_id")

    try:
        room = ChatRoom.objects.get(id=room_id)
    except ChatRoom.DoesNotExist:
        return Response({'message': "Room not found."}, status=status.HTTP_404_NOT_FOUND)
    
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return  Response({'message': "User not found."}, status=status.HTTP_404_NOT_FOUND)
    
    user_chat, created = UserChatRoom.objects.get_or_create(
                chat_room=room,
                user=user
            )
    return Response({'message': "successfully added to chat room."}, status=status.HTTP_201_CREATED)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def bulk_add_users_to_chat_room(request):
    room_id = request.data.get("room_id")
    user_ids = request.data.get("user_ids", []) 

    try:
        room = ChatRoom.objects.get(id=room_id)
    except ChatRoom.DoesNotExist:
        return Response({'message': "Room not found."}, status=status.HTTP_404_NOT_FOUND)
    
    result = {
        'added': [],
        'already_in_room': [],
        'not_found': [],
    }
    for user_id in user_ids:
        user = User.objects.filter(id=user_id).first()
        if not user:
            result['not_found'].append(user_id)
        else:
            user_chat, created = UserChatRoom.objects.get_or_create(
                chat_room=room,
                user=user
            )
            if created:
                result['added'].append(user_id)
            else:
                result['already_in_room'].append(user_id)
    
    return Response({'message': 'added to chat room.', 'result': result}, status=status.HTTP_201_CREATED)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_chat_room_by_user(request):
    pass


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_chat_room_message(request, room_id):
    message = Message.objects.get(chat_room_id=room_id)
    serializer = MessageSerializer(message)
    return Response(serializer.data)
