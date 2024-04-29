import json

import django.db.utils
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from CSChat.wsgi import *

from .models import Message, User, Chat


class ChatConsumer(AsyncWebsocketConsumer):
    @database_sync_to_async
    def create_chat(self, sender, receiver, msg):
        user = User.objects.get(username=sender)
        user2 = User.objects.get(pk=receiver)
        try:
            chat = Chat.objects.create(pk=receiver)
            chat.members.add(user, user2)
            chat.save()
        except django.db.utils.IntegrityError:
            chat = Chat.objects.get(pk=receiver)
        return Message.objects.create(author=user, receiver=user2, chat=chat, message=msg)

    async def connect(self):
        self.room = self.scope['url_route']['kwargs']['room_name']
        await self.channel_layer.group_add(self.room, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room, self.channel_name)

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        sender = text_data_json['sender']
        receiver = text_data_json['receiver']
        await self.channel_layer.group_send(self.room, {
            'type': 'chat_message',
            'message': message,
            'sender': sender,
            'receiver': receiver
        })

    async def chat_message(self, event):
        message = event['message']
        sender = event['sender']
        receiver = event['receiver']
        new_msg = await self.create_chat(sender, receiver, message)  # It is necessary to await creation of messages
        await self.send(text_data=json.dumps({
            'message': new_msg.message,
            'sender': new_msg.author.get_username(),
            'receiver': new_msg.receiver.get_username()
        }))
