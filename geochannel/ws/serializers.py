from rest_framework.serializers import ModelSerializer

from .models import WebSocket


class WebSocketSerializer(ModelSerializer):
    class Meta:
        model = WebSocket
        fields = ('uuid', 'admin_key', 'connection_key', 'open_connection', 'open_sending', 'http_url', 'ws_url')
        read_only_fields = ('uuid', 'admin_key', 'connection_key')
