import json
from channels.generic.websocket import AsyncWebsocketConsumer

class ChatConsumer(AsyncWebsocketConsumer):
    # Присоединение к комнате
    async def connect(self):
        self.room = self.scope['url_route']['kwargs']['room_name']
        await self.channel_layer.group_add(self.room, self.channel_name)
        await self.accept()
    # Покидание комнаты
    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room, self.channel_name)
    # Получение сообщения от клиента
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        await self.channel_layer.group_send(
            self.room,{'type': 'chat_message', 'message': message}
        )
    # Получение сообщения от комнаты
    async def chat_message(self, event):
        message = event['message']
        await self.send(text_data=json.dumps({'message': message}))