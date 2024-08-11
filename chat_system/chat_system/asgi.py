"""
ASGI config for chat_system project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/asgi/
"""

import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from chat import routing
from chat.jwt_middleware import JWTAuthMiddleware


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'chat_system.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket" : JWTAuthMiddleware(
        URLRouter(
            routing.websocket_urlpatterns
        )    
    )
})

ASGI_APPLICATION = 'chat_system.asgi.application'