import json
from channels.generic.websocket import AsyncWebsocketConsumer


class ChatConsumer(AsyncWebsocketConsumer):

    def connect(self):
        self.room = self.scope['url_route']['kwargs']['room_name']
        self.channel_layer.group_add(
            self.room,
            self.channel_name
        )
        self.accept()

    def disconnect(self, close_code):
        self.channel_layer.group_discard(
            self.room,
            self.channel_layer
        )

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]
        username = text_data_json["username"]
        self.channel_layer.group_send(
            self.room, {
                "type": "sendMessage",
                "message": message,
                "username": username,
            })

    def sendMessage(self, event):
        message = event["message"]
        username = event["username"]
        self.send(text_data=json.dumps({"message": message, "username": username}))