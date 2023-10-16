from common.simple_rest.async_api_request import AsyncAPIRequest
from common.simple_rest.async_views.async_simple_post_api_view import AsyncSimplePostAPIView
from common.simple_rest.permissions_checkers.login_permission_checker import LoginPermissionChecker
from common.simple_rest.permissions_checkers.request_data_fields_checker import RequestDataFieldsAPIChecker
from common.type_hints import JSONType
from users.managers.websocket_events_manager.room_websocket_events_manager import RoomWebsocketEventManager


class PostSampleWebsocketView(AsyncSimplePostAPIView):
    @classmethod
    async def check_permitted(cls, request: AsyncAPIRequest, **kwargs) -> None:
        await RequestDataFieldsAPIChecker(['room_id']).async_raise_exception_if_not_valid(request=request)
        await LoginPermissionChecker().async_raise_exception_if_not_valid(await request.future_user)

    @classmethod
    async def run_action(cls, request: AsyncAPIRequest, **kwargs) -> JSONType:
        room_id = request.data['room_id']
        await RoomWebsocketEventManager(room_id=room_id).async_send_event_to_group({'message': 'Hello from websocket!'})
        return {}
