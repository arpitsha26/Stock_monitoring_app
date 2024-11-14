"""
ASGI config for Stock_system project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/asgi/
"""
from channels.routing import ProtocolTypeRouter, URLRouter
import os
from django.urls import path

from django.core.asgi import get_asgi_application
from Home.consumers import * 

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Stock_system.settings')

application = get_asgi_application()

ws_patterns=[
    path('ws/test/', TestConsumer )
    
]

application = ProtocolTypeRouter({
    'websocket': URLRouter(ws_patterns)
})