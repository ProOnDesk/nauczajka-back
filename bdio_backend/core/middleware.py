from django.contrib.auth.models import AnonymousUser
from channels.db import database_sync_to_async
from channels.middleware import BaseMiddleware
from rest_framework_simplejwt.tokens import AccessToken
from user.models import User

@database_sync_to_async
def get_user(token):
    try:
        token = AccessToken(token)
        user_id = token.payload['user_id']
        user = User.objects.get(id=user_id)
        return user
    except Exception as e:
        return None


class CookieMiddleware:
    def __init__(self, inner):
        self.inner = inner

    async def __call__(self, scope, receive, send):
        headers = dict(scope['headers'])
        cookies = {}
        if b'cookie' in headers:
            cookie_header = headers[b'cookie'].decode()
            cookies = {key: value for key, value in [cookie.split('=') for cookie in cookie_header.split('; ')]}
        scope['cookies'] = cookies
        return await self.inner(scope, receive, send)


class TokenAuthMiddleware(BaseMiddleware):
    def __init(self, inner):
        self.inner = inner
    
    async def __call__(self, scope, receive, send):
        cookies = scope.get('cookies', {})
        token = cookies.get('token')
        user = await get_user(token) if token else None

        if user is None:
            return
        
        scope['user'] = user
        
        return await super().__call__(scope, receive, send)
