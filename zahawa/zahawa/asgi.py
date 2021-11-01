"""
ASGI config for zahawa project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/asgi/
"""

import os

from channels.routing import ProtocolTypeRouter, URLRouter
from django.conf.urls import url
from django.core.asgi import get_asgi_application
from django.urls import path
from chat.consumers import MyConsumer

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'zahawa.settings')

ws_patterns = [
    url(r'^ws/test/', MyConsumer.as_asgi())
]

application = get_asgi_application()
application = ProtocolTypeRouter({
    # "http": get_asgi_application(),
    "websocket": URLRouter(ws_patterns)
    # Just HTTP for now. (We can add other protocols later.)
})


