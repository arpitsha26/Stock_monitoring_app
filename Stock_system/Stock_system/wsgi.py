"""
WSGI config for Stock_system project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/wsgi/
"""
from channels.routing import ProtocolTypeRouter, URLRouter
import os

from django.core.wsgi import get_wsgi_application
from django.urls import path

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Stock_system.settings')

application = get_wsgi_application()

ws_patterns=[
    path('test/', )
    
]

application = ProtocolTypeRouter({
    'websocket': URLRouter(ws_patterns)
})