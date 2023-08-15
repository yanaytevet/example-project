from typing import Set, Type

from django.db.models import Model

from common.simple_rest.async_api_request import AsyncAPIRequest
from common.simple_rest.async_views.async_post_create_api_view import AsyncPostCreateAPIView
from common.simple_rest.permissions_checkers.login_permission_checker import LoginPermissionChecker
from common.type_hints import JSONType
from users.models import UserEvent
from users.tasks.run_events_analysis import run_events_analysis


class PostCreateUserEventView(AsyncPostCreateAPIView):
    @classmethod
    async def check_permitted(cls, request: AsyncAPIRequest, **kwargs) -> None:
        pass

    @classmethod
    def get_allowed_creation_fields(cls) -> Set[str]:
        return {'name', 'tab_id', 'attributes', 'user_id'}

    @classmethod
    async def serialize_object(cls, request: AsyncAPIRequest, obj: Model, **kwargs) -> JSONType:
        return {}

    @classmethod
    def get_model_cls(cls) -> Type[Model]:
        return UserEvent

    @classmethod
    async def modify_creation_data(cls, request: AsyncAPIRequest,  data: JSONType) -> JSONType:
        if await request.async_get_as_other():
            return {}
        user = await request.future_user
        data['user_id'] = user.id if LoginPermissionChecker().is_valid(user) else None
        return data

    @classmethod
    async def run_after_post(cls, request: AsyncAPIRequest,  obj: Model, **kwargs) -> None:
        if obj and obj.id:
            run_events_analysis.delay(obj.id)
