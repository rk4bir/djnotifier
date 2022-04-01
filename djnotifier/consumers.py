# djnotifier/consumers.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer


class DJNotifierConsumer(AsyncWebsocketConsumer):

    async def connect(self) -> None:
        user = self.scope["user"]
        group = "dj_notifier_anonymous"
        if not user.is_anonymous:
            group = f"dj_notifier_{user.pk}"

        self.group_name = group

        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )
        self.groups.append(self.group_name)
        await self.accept()

    async def disconnect(self, close_code) -> None:
        await self.channel_layer.group_discard(self.group_name, self.channel_name)
        self.groups.remove(self.group_name)
        await self.close()

    async def receive(self, text_data=None, bytes_data=None) -> None:
        pass

    async def dj_notifier(self, event):
        data = event["data"]
        await self.send(text_data=json.dumps(data))
