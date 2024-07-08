from django.urls import path
from notification.consumers import NotificationConsumer

websocket_urlpatterns = [
    path('ws/notification/user/', NotificationConsumer.as_asgi()),
]
