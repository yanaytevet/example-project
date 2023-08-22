import json
from typing import Optional

from channels.generic.websocket import AsyncWebsocketConsumer

from common.simple_rest.permissions_checkers.login_permission_checker import LoginPermissionChecker
from users.models import User


class UserWebsocketConsumer(AsyncWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user_group_name: Optional[str] = None

    @classmethod
    async def check_permitted(cls, user: User) -> None:
        await LoginPermissionChecker().async_raise_exception_if_not_valid(user)

    async def connect(self):
        user_id = self.scope['user'].id
        self.user_group_name = f'user_{user_id}'
        await self.check_permitted(self.scope['user'])
        await self.channel_layer.group_add(self.user_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.user_group_name,
            self.channel_name
        )

    async def receive(self, text_data=None, bytes_data=None):
        pass

    async def send_event_to_user(self, event) -> None:
        await self.send(text_data=json.dumps(event['data']))
