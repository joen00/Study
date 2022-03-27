from commons.chat_history_handler import add_chat
import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer


import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

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
        message = text_data_json['message']
        add_chat(text_data_json['room_name'],
                 text_data_json['chatter'], message)
        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )

    # Receive message from room group
    def chat_message(self, event):
        message = event['message']

        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'message': message
        }))


f.send(text_data=json.dumps({
    'message': message
}))
f.send(text_data=json.dumps({
    'message': message
}))
f.send(text_data=json.dumps({
    'message': message
}))
