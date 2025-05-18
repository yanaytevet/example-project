from typing import Type

from django.contrib.auth.models import User
from ninja import Schema, Path, Query

from common.simple_api.api_request import APIRequest
from common.simple_api.views.simple_get_api_view import SimpleGetAPIView
from users.schemas.auth_schema import AuthSchema
from users.serializers.user.user_serializer import UserSerializer


class AuthView(SimpleGetAPIView):
    @classmethod
    def get_output_schema(cls) -> Type[Schema]:
        return AuthSchema

    @classmethod
    async def check_permitted(cls, request: APIRequest, query: Query = None, path: Path = None) -> None:
        pass

    @classmethod
    async def get_data(cls, request: APIRequest, query: Query = None, path: Path = None) -> AuthSchema:
        data = AuthSchema(is_authenticated=False, user=None)
        user_obj = await request.future_user
        if cls.is_active_user(user_obj):
            data.is_authenticated = True
            data.user = await UserSerializer().serialize(user_obj)
        return data

    @classmethod
    def is_active_user(cls, user_obj: User) -> bool:
        return user_obj and not user_obj.is_anonymous
