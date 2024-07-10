from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import sync_to_async
import json
from .models import *
from django.template.loader import render_to_string
from django.shortcuts import get_object_or_404
from asgiref.sync import async_to_sync

class ChatRoomConsumer(WebsocketConsumer):
    def connect(self):
        self.user = self.scope['user']
        self.chatroom_name = self.scope['url_route']['kwargs']['chatroom_name']
        self.chatroom = get_object_or_404(ChatGroup, group_name=self.chatroom_name)
        
        async_to_sync(self.channel_layer.group_add)(
            self.chatroom_name,
            self.channel_name
        )
        self.accept()
    
        if not self.user in self.chatroom.users_online.all():
            self.chatroom.users_online.add(self.user)
            self.update_online_users_count()
    
    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.chatroom_name,
            self.channel_name
        )
        if self.user in self.chatroom.users_online.all():
            self.chatroom.users_online.remove(self.user)
            self.update_online_users_count()

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        body = text_data_json['body']
        message = GroupMessage.objects.create(
            group=self.chatroom,
              author=self.user, 
              body=body,
              )
        event = {
            'type':'message_handler',
            'message_id':message.id,
        }
        

        async_to_sync(self.channel_layer.group_send)(
            self.chatroom_name, event
        )
    def message_handler(self, event):
        message_id = event['message_id']
        message = GroupMessage.objects.get(id=message_id)
        context = {'message':message, 'user':self.user}
        html = render_to_string('a_rtchat/partials/chat_message_p.html', context=context)
        self.send(text_data=html)
    def update_online_users_count(self):
        event = {
            'type':'online_users_count',
            'count':self.chatroom.users_online.count(),
        }
        async_to_sync(self.channel_layer.group_send)(
            self.chatroom_name, event
        )
    def online_users_count(self, event):
        count = event['count']
        html = render_to_string('a_rtchat/partials/online_count.html',{'online_count':count})
        self.send(text_data=html)
        

