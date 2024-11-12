# chat/routing.py
from django.urls import re_path
from.consumers import Consumers

websocket_urlpatterns = [
    re_path(r'ws/chat/$',Consumers.as_asgi()),
]
