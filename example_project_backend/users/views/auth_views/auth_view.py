from django.contrib.auth.models import User

from common.simple_rest.async_api_request import AsyncAPIRequest
from common.simple_rest.async_views.async_simple_get_api_view import AsyncSimpleGetAPIView
from common.type_hints import JSONType
from users.serializers.user.user_serializer import UserSerializer


class AuthView(AsyncSimpleGetAPIView):
    @classmethod
    async def check_permitted(cls, request: AsyncAPIRequest, **kwargs) -> None:
        pass

    @classmethod
    async def get_data(cls, request: AsyncAPIRequest, **kwargs) -> JSONType:
        data = {
            'is_auth': False,
        }
        user_obj = await request.future_user
        if cls.is_active_user(user_obj):
            data['is_auth'] = True
            serializer = UserSerializer()
            data['user'] = serializer.serialize(user_obj)
        else:
            data['user'] = None
        return data

    @classmethod
    def is_active_user(cls, user_obj: User) -> bool:
        return user_obj and not user_obj.is_anonymous
