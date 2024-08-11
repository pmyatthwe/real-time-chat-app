import jwt
from channels.middleware import BaseMiddleware
from rest_framework_simplejwt.tokens import AccessToken
from channels.db import database_sync_to_async
from django.conf import settings
from .enums import JwtError


class JWTAuthMiddleware(BaseMiddleware):

    def __init__(self, inner):
        self.inner = inner
        self.secret_key = settings.SECRET_KEY 
    
    async def __call__(self, scope, receive, send):
        token = self.get_token_from_scope(scope)
        if token != None:
            user_id = await self.get_user_from_token(token) 
            if user_id:
                scope['user_id'] = user_id
            else:
                scope['error'] = JwtError.INVALID
        if token == None:
            scope['error'] = JwtError.NO_TOKEN
        return await super().__call__(scope, receive, send)
    

    def get_token_from_scope(self, scope):
        headers = dict(scope.get("headers", []))
        auth_header = headers.get(b'authorization', b'').decode('utf-8')
        if auth_header.startswith('Bearer '):
            return auth_header.split(' ')[1]
        else:
            return None
        
    @database_sync_to_async
    def get_user_from_token(self, token):
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=["HS256"])
            return payload['user_id']
        except:
            return None
