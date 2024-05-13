from django.urls import path
from .consumers import MouseDataConsumer

websocket_urlpatterns = [
    path('ws/mouse/', MouseDataConsumer.as_asgi()),
]
