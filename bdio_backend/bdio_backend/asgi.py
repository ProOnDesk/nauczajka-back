"""
ASGI config for bdio project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
"""

import os
import django
django.setup()

from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from chat import routing as chat_routing
from notification import routing as notification_routing
from core.middleware import TokenAuthMiddleware, CookieMiddleware

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bdio_backend.settings')

django_asgi_app = get_asgi_application()

application = ProtocolTypeRouter({
    'http': django_asgi_app,
    'websocket': AllowedHostsOriginValidator(
        CookieMiddleware(
            TokenAuthMiddleware(
                URLRouter(
                    chat_routing.websocket_urlpatterns + notification_routing.websocket_urlpatterns
                )
            )
        )
    ),
})
