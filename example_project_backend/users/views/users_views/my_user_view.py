from common.simple_rest.async_api_request import AsyncAPIRequest
from common.simple_rest.async_views.async_get_item_api_view import AsyncGetItemAPIView
from common.simple_rest.permissions_checkers.login_permission_checker import LoginPermissionChecker
from common.type_hints import JSONType
from users.models import User
from users.serializers.user.user_serializer import UserSerializer


class MyUserItemView(AsyncGetItemAPIView):

    @classmethod
    async def check_permitted_before_object(cls, request: AsyncAPIRequest, **kwargs) -> None:
        user_obj = await request.future_user
        await LoginPermissionChecker().async_raise_exception_if_not_valid(user_obj)

    @classmethod
    async def get_object(cls, request: AsyncAPIRequest, **kwargs) -> User:
        return await request.future_user

    @classmethod
    async def check_permitted_after_object(cls, request: AsyncAPIRequest, obj: User, **kwargs) -> None:
        pass

    @classmethod
    async def serialize_object(cls, request: AsyncAPIRequest, obj: User, **kwargs) -> JSONType:
        return UserSerializer().serialize(obj)
