from django.urls import path

from .consumers import CustomJsonConsumer

websocket_urlpatterns = [
    path('wss/<uuid:uuid>/', CustomJsonConsumer),
]
