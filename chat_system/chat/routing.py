from django.urls import re_path, path
from chat.consumers import ChatConsumer

websocket_urlpatterns = [
    re_path(r'ws/chat/(?P<room_name>\w+)/$', ChatConsumer.as_asgi()),
]


# websocket_urlpatterns = [
#     path('ws/chat/<int:room_id>/', ChatConsumer.as_asgi()),
# ]