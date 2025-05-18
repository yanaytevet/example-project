from typing import Type

from ninja import Schema, Path

from common.simple_api.api_request import APIRequest
from common.simple_api.permissions_checkers.login_permission_checker import LoginPermissionChecker
from common.simple_api.schemas.empty_schema import EmptySchema
from common.simple_api.views.simple_post_api_view import SimplePostAPIView
from users.managers.django_auth import DjangoAuth
from users.schemas.auth_schema import AuthSchema


class LogoutView(SimplePostAPIView):
    @classmethod
    def get_output_schema(cls) -> Type[Schema]:
        return AuthSchema

    @classmethod
    def get_data_schema(cls) -> Type[Schema]:
        return EmptySchema

    @classmethod
    async def check_permitted(cls, request: APIRequest, data: EmptySchema, path: Path = None) -> None:
        await LoginPermissionChecker().async_raise_exception_if_not_valid(await request.future_user)

    @classmethod
    async def run_action(cls, request: APIRequest, data: EmptySchema, path: Path = None) -> AuthSchema:
        await DjangoAuth.async_logout(request)
        return AuthSchema(is_authenticated=False, user=None)
