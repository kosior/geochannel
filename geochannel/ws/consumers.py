from asgiref.sync import async_to_sync
from channels.generic.websocket import JsonWebsocketConsumer

from .models import WebSocket
from .utils import get_token_from_query_string


class CustomJsonConsumer(JsonWebsocketConsumer):
    def connect(self):
        self.group_name = str(self.scope['url_route']['kwargs']['uuid'])
        token = get_token_from_query_string(self.scope['query_string'].decode())

        self.ws_object = WebSocket.objects.get_with_permissions(uuid=self.group_name, token=token)

        if self.ws_object and self.ws_object.connect_permission:
            async_to_sync(self.channel_layer.group_add)(self.group_name, self.channel_name)
            self.accept()
        else:
            self.close()

    def disconnect(self, code):
        async_to_sync(self.channel_layer.group_discard)(
            self.group_name,
            self.channel_name
        )

    def receive_json(self, content, **kwargs):
        if self.ws_object.send_permission:
            async_to_sync(self.channel_layer.group_send)(self.group_name, {'type': 'json.message', 'content': content})
        else:
            self.send_json({'error': 'Sending not allowed.'})

    def json_message(self, event):
        content = event['content']
        self.send_json(content)

    def force_disconnect(self, event):
        self.close()
