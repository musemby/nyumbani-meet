"""
ASGI config for zoloni project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/howto/deployment/asgi/
"""

# import os

# from django.core.asgi import get_asgi_application

# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'zoloni.settings')

# application = get_asgi_application()

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django_application = get_asgi_application()

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter


from users.middleware import TokenAuthMiddlewareStack


application = ProtocolTypeRouter({
    "http": django_application,
    "websocket": TokenAuthMiddlewareStack(
        URLRouter(
            realtime.routing.websocket_urlpatterns
        )
    )
})
