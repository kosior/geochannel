from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from .auth import WsTokenHeaderAuth
from .serializers import WebSocketSerializer


class CreateWebSocket(CreateAPIView):
    serializer_class = WebSocketSerializer
    # authentication_classes = []
    # permission_classes = []


class SendContent(APIView):
    authentication_classes = [WsTokenHeaderAuth]
    # permission_classes = []

    def post(self, request, *args, **kwargs):
        uuid = str(kwargs.get('uuid'))
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(uuid, {
            'type': 'json.message',
            'content': request.data
        })
        return Response()
