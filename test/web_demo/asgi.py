"""
ASGI config for web_demo project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/asgi/
"""

import os



os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'web_demo.settings')
from django.core.asgi import get_asgi_application

from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
import yourapp.routing
django_asgi_app = get_asgi_application()

application = ProtocolTypeRouter({
    'websocket': AuthMiddlewareStack(
        URLRouter(
            yourapp.routing.websocket_urlpatterns
        )
    ),
})
