from common.simple_rest.async_api_request import AsyncAPIRequest
from common.simple_rest.async_views.async_simple_post_api_view import AsyncSimplePostAPIView
from common.simple_rest.permissions_checkers.login_permission_checker import LoginPermissionChecker
from common.simple_rest.permissions_checkers.request_data_fields_checker import RequestDataFieldsAPIChecker
from common.type_hints import JSONType
from users.managers.websocket_events_manager.websocket_event_manager import WebsocketEventManager


class PostSampleBlockView(AsyncSimplePostAPIView):
    @classmethod
    async def check_permitted(cls, request: AsyncAPIRequest, **kwargs) -> None:
        await RequestDataFieldsAPIChecker(['event_type']).async_raise_exception_if_not_valid(request=request)
        await LoginPermissionChecker().async_raise_exception_if_not_valid(await request.future_user)

    @classmethod
    async def run_action(cls, request: AsyncAPIRequest, **kwargs) -> JSONType:
        event_type = request.data['event_type']
        user = await request.future_user
        await WebsocketEventManager.async_send_event_to_user(user, event_type, {'message': 'Hello from websocket!'})
        return {}
