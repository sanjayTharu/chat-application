from channels.consumer import AsyncConsumer,SyncConsumer
from channels.exceptions import StopConsumer
import json
import asyncio
from time import sleep
from asgiref.sync import async_to_sync

class MySyncConsumer(SyncConsumer):

    def websocket_connect(self,event):
        print('Websocket Conneted...',event)
        print("channel Layer...",self.channel_layer)#get default channel layer from project
        print("channel Name...",self.channel_name)#get channel name
        self.group_name=self.scope['url_route']['kwargs']['groupName']
        print('Group Name:',self.group_name)
        
        async_to_sync(self.channel_layer.group_add)(
            self.group_name, #groupname
            self.channel_name
            )
        self.send({
            'type':'websocket.accept'
        })
    def websocket_receive(self,event):
        print('Message received from client',event['text'])
        print('Type of Message received from client',type(event['text']))

        async_to_sync(self.channel_layer.group_send)(
            self.group_name,
            {
                'type':'chat.message',
                'message':event['text']
        })

    def chat_message(self,event):
        print('Event...',event)
        print('Actual Message...',event['message'])
        print('Type of Actual Message...',type(event['message']))
        self.send({
            'type':'websocket.send',
            'text': event['message']
        })

    def websocket_disconnect(self,event):
        print('Websocket Disconnected...',event)
        print("channel Layer...",self.channel_layer)#get default channel layer
        print("channel name...",self.channel_name)#get channel Name
        async_to_sync(self.channel_layer.group_discard)(
            self.group_name,
            self.channel_name
        )
        raise StopConsumer()
        
class MyAsyncConsumer(AsyncConsumer):

    async def websocket_connect(self,event):
        print('Websocket Conneted...',event)
        print("channel Layer...",self.channel_layer)#get default channel layer from project
        print("channel Name...",self.channel_name)#get channel name
        self.group_name=self.scope['url_route']['kwargs']['groupName']
        print('Group Name:',self.group_name)
        await self.channel_layer.group_add(
            self.group_name, #groupname
            self.channel_name
            )
        await self.send({
            'type':'websocket.accept'
        })
    async def websocket_receive(self,event):
        print('Message received from client',event['text'])
        print('Type of Message received from client',type(event['text']))

        await self.channel_layer.group_send(
            self.group_name,
            {
                'type':'chat.message',
                'message':event['text']
        })

    async def chat_message(self,event):
        print('Event...',event)
        print('Actual Message...',event['message'])
        print('Type of Actual Message...',type(event['message']))
        await self.send({
            'type':'websocket.send',
            'text': event['message']
        })

    async def websocket_disconnect(self,event):
        print('Websocket Disconnected...',event)
        print("channel Layer...",self.channel_layer)#get default channel layer
        print("channel name...",self.channel_name)#get channel Name
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )
        raise StopConsumer()
   