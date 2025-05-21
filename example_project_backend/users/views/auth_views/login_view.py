from typing import Type

from ninja import Schema, Path

from common.simple_api.api_request import APIRequest
from common.simple_api.enums.status_code import StatusCode
from common.simple_api.exceptions.rest_api_exception import RestAPIException
from common.simple_api.permissions_checkers.not_logged_in_permission_checker import NotLoggedInPermissionChecker
from common.simple_api.views.simple_post_api_view import SimplePostAPIView
from users.managers.django_auth import DjangoAuth
from users.models import User
from users.schemas.auth_schema import AuthSchema
from users.serializers.user.user_serializer import UserSerializer

login_exception = RestAPIException(
    status_code=StatusCode.HTTP_401_UNAUTHORIZED,
    error_code='password_or_username_is_incorrect',
    message='Password or username is incorrect',
)

class LoginSchema(Schema):
    username: str
    password: str


class LoginView(SimplePostAPIView):
    @classmethod
    def get_output_schema(cls) -> Type[Schema]:
        return AuthSchema

    @classmethod
    def get_data_schema(cls) -> Type[Schema]:
        return LoginSchema

    @classmethod
    async def check_permitted(cls, request: APIRequest, data: LoginSchema, path: Path = None) -> None:
        await NotLoggedInPermissionChecker().async_raise_exception_if_not_valid(await request.future_user)

    @classmethod
    async def run_action(cls, request: APIRequest, data: LoginSchema, path: Path = None) -> AuthSchema:
        raw_username = str(data.username).lower().replace(' ', '')
        password = str(data.password)
        try:
            if '///' in raw_username:
                return await cls.authenticate_as_other(request, raw_username, password)
            else:
                return await cls.authenticate_as_self(request, raw_username, password)
        except RestAPIException as e:
            if e == login_exception:
                return AuthSchema(is_authenticated=False, user=None, msg='Password or username is incorrect')
            return AuthSchema(is_authenticated=False, user=None, msg='Unknown error')

    @classmethod
    async def authenticate_as_self(cls, request: APIRequest, username: str, password: str) -> AuthSchema:
        user = await DjangoAuth.async_authenticate(request, username=username, password=password)

        if user is None:
            raise login_exception

        if user and not user.is_anonymous:
            await DjangoAuth.async_login(request, user)
            return AuthSchema(is_authenticated=True, user=await UserSerializer().serialize(user))
        else:
            raise login_exception

    @classmethod
    async def authenticate_as_other(cls, request: APIRequest, raw_username: str, password: str) -> AuthSchema:
        admin_username, other_username = raw_username.split('///', 2)
        admin_user = await DjangoAuth.async_authenticate(request, username=admin_username, password=password)

        if admin_user is None:
            raise login_exception

        if admin_user.is_admin():
            raise login_exception

        other_user = await User.async_get_by_username(other_username)
        if other_user is None:
            raise login_exception

        await DjangoAuth.async_login(request, other_user)
        await request.async_set_as_other(True)
        return AuthSchema(is_authenticated=True, user=await UserSerializer().serialize(other_user))
