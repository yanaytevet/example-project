from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

from common.type_hints import JSONType
from users.models import User


class WebsocketEventManager:

    @classmethod
    async def async_send_event_to_user(cls, user: User, event_type: str, data: JSONType) -> None:
        group_id = f'user_{user.id}'
        channel_layer = get_channel_layer()
        await channel_layer.group_send(
            group_id,
            {
                'data': {
                    'event_type': event_type,
                    'payload': data
                },
                'type': 'send_event_to_user',
            }
        )
