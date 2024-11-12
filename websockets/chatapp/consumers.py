# chat/consumers.py
from datetime import datetime, timezone
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import *
from channels.db import database_sync_to_async

class Consumers(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        print("server connected")

    async def receive(self, text_data):
        print("testing",text_data)
        data = json.loads(text_data)
        
        sender = data['sender']
        receiver = data['receiver']
        message= data['message']

        sender_name = await self.get_sender_name(sender)

        message_box = MassageBox(sender_id=sender, receiver_id=receiver, message=message)
        await database_sync_to_async(message_box.save)()

        await self.send_message_to_user(receiver, sender_name, message)

    async def send_message_to_user(self, receiver, sender_name, message):

        await self.send(text_data=json.dumps({
            'sender': sender_name,
            'receiver': receiver,
            'message': message,
        }))

    
    async def disconnect(self, close_code):
        print("disconnect")

    async def get_sender_name(self, sender_id):
        user = await database_sync_to_async(User.objects.get)(id=sender_id)
        return user.name