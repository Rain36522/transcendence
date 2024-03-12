import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
import myApp.routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myProject.settings')

application = ProtocolTypeRouter({
  "http": get_asgi_application(),
  # Just HTTP for now. (We can add other protocols later.)
  "websocket": AuthMiddlewareStack(
      URLRouter(
          myApp.routing.websocket_urlpatterns
      )
  ),
})
