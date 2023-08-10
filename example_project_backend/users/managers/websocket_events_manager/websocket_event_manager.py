import json

from asgiref.sync import async_to_sync

from common.type_hints import JSONType
from users.models import User
from channels.layers import get_channel_layer


class WebsocketEventManager:

    @classmethod
    def send_event_to_users(cls, users: list[User], action_name: str, data: JSONType) -> None:
        for target_user in users:
            cls.send_event_to_user(target_user, action_name, data)

    @classmethod
    def send_event_to_user(cls, user: User, action_name: str, data: JSONType) -> None:
        group_id = f'user_{user.id}'
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            group_id,
            {
                'data': {
                    'action': action_name,
                    'payload': data
                },
                'type': 'send_event_to_user',
            }
        )
