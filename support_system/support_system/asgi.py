import os

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application

import chat_app.web_socket.routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'support_system.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            chat_app.web_socket.routing.websocket_urlpatterns
        )
    ),
})