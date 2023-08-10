
from common.django_utils.django_auth import DjangoAuth
from common.simple_rest.async_api_request import AsyncAPIRequest
from common.simple_rest.async_views.async_simple_post_api_view import AsyncSimplePostAPIView
from common.simple_rest.constants.status_code import StatusCode
from common.simple_rest.exceptions.rest_api_exception import RestAPIException
from common.simple_rest.permissions_checkers.not_logged_in_permission_checker import NotLoggedInPermissionChecker
from common.simple_rest.permissions_checkers.request_data_fields_checker import RequestDataFieldsAPIChecker
from common.type_hints import JSONType
from users.models import User
from users.serializers.user.user_serializer import UserSerializer


login_exception = RestAPIException(
    status_code=StatusCode.HTTP_401_UNAUTHORIZED,
    error_code='password_or_username_is_incorrect',
    message='Password or username is incorrect',
)


class LoginView(AsyncSimplePostAPIView):
    @classmethod
    async def check_permitted(cls, request: AsyncAPIRequest, **kwargs) -> None:
        await NotLoggedInPermissionChecker().async_raise_exception_if_not_valid(request=request)
        await RequestDataFieldsAPIChecker(['username', 'password']).async_raise_exception_if_not_valid(request=request)

    @classmethod
    async def run_action(cls, request: AsyncAPIRequest, **kwargs) -> JSONType:
        raw_username = str(request.data['username']).lower().replace(' ', '')
        password = str(request.data['password'])
        if '///' in raw_username:
            return await cls.authenticate_as_other(request, raw_username, password)
        else:
            return await cls.authenticate_as_self(request, raw_username, password)

    @classmethod
    async def authenticate_as_self(cls, request: AsyncAPIRequest, username: str, password: str) -> JSONType:
        user = await DjangoAuth.async_authenticate(request, username=username, password=password)

        if user is None:
            raise login_exception

        if user and not user.is_anonymous:
            await DjangoAuth.async_login(request, user)
            request.set_as_other(False)
            return {'is_auth': True, 'msg': '', 'user': UserSerializer().serialize(user)}
        else:
            raise login_exception

    @classmethod
    async def authenticate_as_other(cls, request: AsyncAPIRequest, raw_username: str, password: str) -> JSONType:
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
        request.set_as_other(True)
        return {'is_auth': True, 'msg': '', 'user': UserSerializer().serialize(other_user)}
