from django.urls import path
from . import consumers


websocket_urlpatterns = [
    path('chat/chats/', consumers.ChatConsumer.as_asgi()),
]