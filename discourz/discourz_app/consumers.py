from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from django.contrib.auth.models import User
from datetime import datetime
from discourz_app.models import Account, PollTopic, Debates, PastDebates, Chat, Comment, DebateMessage
import json

class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name
        self.user = self.scope["user"]

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = (text_data_json['message'])
        debateId = (text_data_json['debateId'])

        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'username': self.scope["user"].username,
                'debateId':debateId,
                'userAvatar': self.scope["user"].account.img.url,
            }
        )
        print(debateId)
        newMessage = DebateMessage(message,self.scope["user"].id,datetime.now())
        #newMessage.save()

    # Receive message from room group
    def chat_message(self, event):
        message = event['message']
        username = event['username']
        avatar = event['userAvatar']
        

        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'message': message,
            'username':username,
            'avatar':avatar
        }))