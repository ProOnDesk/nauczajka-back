from django.urls import re_path
from chat.consumers import ChatConsumer, ChatListConsumer

websocket_urlpatterns = [
    re_path(r'ws/chat/list/$', ChatListConsumer.as_asgi()),
    re_path(r'^ws/chat/(?P<conversation_id>[^/]+)/$', ChatConsumer.as_asgi())
]
