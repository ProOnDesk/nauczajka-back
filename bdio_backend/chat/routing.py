from django.urls import re_path
from chat.consumers import ChatConsumer
from notification.consumers import NotificationConsumer

websocket_urlpatterns = [
    re_path(r'^ws/chat/(?P<conversation_id>[^/]+)/$', ChatConsumer.as_asgi()),
]
