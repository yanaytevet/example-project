from django.urls import path

from users.consumers.user_websocket_consumer import UserWebsocketConsumer

websocket_urlpatterns = [
   path(r'ws/socket/', UserWebsocketConsumer.as_asgi()),
]
