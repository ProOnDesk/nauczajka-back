from django.urls import path
from . import consumers
from rest_framework.schemas import get_schema_view

websocket_urlpatterns = [
    path('ws/chat/<uuid:conversation_id>/', consumers.ChatConsumer.as_asgi()),
]
