from django.urls import re_path
from .import consumers

websocket_urlpatterns=[
re_path('ws/socket/', consumers.TestConsumer.as_asgi())    
]
