from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import sync_to_async
import json
from .models import *
from django.shortcuts import get_object_or_404

class ChatRoomConsumer(WebsocketConsumer):
    def connect(self):
        self.user = self.scope['user']
        self.chatroom_name = self.scope['url_route']['kwargs']['chatroom_name']
        self.chatroom = get_object_or_404(ChatGroup, group_name=self.chatroom_name)
        self.accept()

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        body = text_data_json['body']
        message = GroupMessage.objects.create(
            group=self.chatroom,
              author=self.user, 
              body=body,
              )

