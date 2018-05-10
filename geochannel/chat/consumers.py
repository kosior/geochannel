import json

from channels.generic.websocket import AsyncWebsocketConsumer


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = 'main'
        self.room_group_name = f'chat_{self.room_name}'

        await self.channel_layer.group_add(self.room_group_name, self.channel_name)

        await self.accept()

    async def disconnect(self, code):
        await self.channel_layer.group_discard(
            self.room_group_name, self.channel_name
        )

    async def receive(self, text_data=None, bytes_data=None):
        text_data_json = json.loads(text_data)
        name = text_data_json['name']
        latlng = text_data_json['latlng']
        message = text_data_json['message']

        await self.channel_layer.group_send(
            self.room_group_name,
            {'type': 'chat_message', 'message': message, 'latlng': latlng, 'name': name}
        )

    async def chat_message(self, event):
        name = event['name']
        latlng = event['latlng']
        message = event['message']
        await self.send(text_data=json.dumps({'message': message, 'latlng': latlng, 'name': name}))
