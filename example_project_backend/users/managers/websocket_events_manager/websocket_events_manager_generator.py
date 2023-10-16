from common.type_hints import JSONType
from users.managers.websocket_events_manager.base_websocket_events_manager import BaseWebsocketEventsManager
from users.managers.websocket_events_manager.room_websocket_events_manager import RoomWebsocketEventManager


class WebsocketEventsManagerGenerator:
    EVENT_TYPE_TO_CLS = {
        'room': RoomWebsocketEventManager,
    }

    @classmethod
    def generate(cls, event_type: str, additional_info: JSONType) -> BaseWebsocketEventsManager:
        return cls.EVENT_TYPE_TO_CLS[event_type].generate_from_additional_info(additional_info)
