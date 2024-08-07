from django.urls import path
from django.urls import re_path
from notification.consumers import NotificationConsumer
websocket_urlpatterns = [
    re_path(r'^ws/notification/user/$', NotificationConsumer.as_asgi()),
]
