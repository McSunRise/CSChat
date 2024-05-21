from django.urls import path
from chat.consumer import ChatConsumer, HomeConsumer

websocket_urlpatterns = [
    path('ws/chat', HomeConsumer.as_asgi()),
    path('ws/chat/<str:room_name>/', ChatConsumer.as_asgi()),
]