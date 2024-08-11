from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .models import ChatRoom, UserChatRoom, Message
from users.models import User
from .serializers import MessageSerializer, ChatRoomSerializer


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_chat_rooms(request):
    chat_rooms = ChatRoom.objects.all().prefetch_related('online')
    serializer = ChatRoomSerializer(chat_rooms, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_chat_room_detail(request, chat_room_id):
    try:
        chat_room = ChatRoom.objects.prefetch_related('online').get(id=chat_room_id)
    except ChatRoom.DoesNotExist:
        return Response({"message": "Chat room not found."}, status=status.HTTP_404_NOT_FOUND)
    
    serializer = ChatRoomSerializer(chat_room)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_all_users_in_chat_room(request, chat_room_id):
    try:
        chat_room = ChatRoom.objects.get(id=chat_room_id)
    except ChatRoom.DoesNotExist:
        return Response({"message": "Chat room not found."}, status=status.HTTP_404_NOT_FOUND)

    user_chat_rooms = UserChatRoom.objects.select_related('user').filter(chat_room=chat_room)
    users = [user_chat_room.user for user_chat_room in user_chat_rooms if user_chat_room.user is not None]
    user_data = [{"id": user.id, "username": user.username} for user in users]
    return Response(user_data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_chat_room_message(request, chat_room_id):
    try:
        message = Message.objects.get(chat_room_id=chat_room_id)
    except Message.DoesNotExist:
        return Response({"message": "No message found."}, status=status.HTTP_404_NOT_FOUND)
    
    serializer = MessageSerializer(message)
    return Response(serializer.data, status=status.HTTP_200_OK)


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
def add_user_to_chat_room(request, chat_room_id):
    user_id = request.data.get("user_id")

    try:
        room = ChatRoom.objects.get(id=chat_room_id)
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


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def delete_user_from_chat_room(request, chat_room_id):
    try:
        chat_room = ChatRoom.objects.get(id=chat_room_id)
    except ChatRoom.DoesNotExist:
        return Response({"detail": "Chat room not found."}, status=status.HTTP_404_NOT_FOUND)
    user_id = request.data.get("user_id")
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return  Response({'message': "User not found."}, status=status.HTTP_404_NOT_FOUND)
    
    user_chat_room = UserChatRoom.objects.filter(user=user, chat_room=chat_room).first()
    if not user_chat_room:
        return Response({"message": "User does not exist in this chat room."}, status=status.HTTP_400_BAD_REQUEST)
    user_chat_room.delete()
    return Response({"message": "User removed from chat room."}, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def delete_chat_room(request, chat_room_id):
    try:
        chat_room = ChatRoom.objects.get(id=chat_room_id)
    except ChatRoom.DoesNotExist:
        return Response({"message": "Chat room not found."}, status=status.HTTP_404_NOT_FOUND)
    
    chat_room.delete()
    return Response({"message": "Chat room deleted."}, status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_chat_room_by_user(request, user_id):
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return Response({"message": "User not found."}, status=status.HTTP_404_NOT_FOUND)

    user_chat_rooms = UserChatRoom.objects.select_related('chat_room').filter(user=user)
    chat_rooms = [user_chat_room.chat_room for user_chat_room in user_chat_rooms]

    if not chat_rooms:
        return Response({"message": "No chat rooms found for this user."}, status=status.HTTP_404_NOT_FOUND)

    serializer = ChatRoomSerializer(chat_rooms, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)
