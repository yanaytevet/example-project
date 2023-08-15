from users.managers.django_auth import DjangoAuth
from common.simple_rest.async_api_request import AsyncAPIRequest
from common.simple_rest.async_views.async_simple_post_api_view import AsyncSimplePostAPIView
from common.simple_rest.constants.status_code import StatusCode
from common.simple_rest.exceptions.rest_api_exception import RestAPIException
from common.simple_rest.permissions_checkers.login_permission_checker import LoginPermissionChecker
from common.simple_rest.permissions_checkers.request_data_fields_checker import RequestDataFieldsAPIChecker
from common.type_hints import JSONType
from users.models import UserEvent


class ChangePasswordView(AsyncSimplePostAPIView):
    @classmethod
    async def check_permitted(cls, request: AsyncAPIRequest, **kwargs) -> None:
        user_obj = await request.future_user
        await RequestDataFieldsAPIChecker(['old_password', 'new_password']).async_raise_exception_if_not_valid(
            request=request)
        await LoginPermissionChecker().async_raise_exception_if_not_valid(user_obj)

    @classmethod
    async def run_action(cls, request: AsyncAPIRequest, **kwargs) -> JSONType:
        user_obj = await request.future_user

        RequestDataFieldsAPIChecker(['old_password', 'new_password']).raise_exception_if_not_valid(request=request)
        LoginPermissionChecker().raise_exception_if_not_valid(user_obj)

        old_pass = str(request.data['old_password'])
        user = await DjangoAuth.async_authenticate(request, username=user_obj.username, password=old_pass)

        if user:
            new_pass = str(request.data['new_password'])
            user.set_password(new_pass)
            await user.asave()
            await UserEvent(name='change_my_password', user=user).asave()
            return {'is_success': True, 'msg': 'Password successfully changed'}

        else:
            raise RestAPIException(
                status_code=StatusCode.HTTP_401_UNAUTHORIZED,
                error_code='password_is_incorrect_correct',
                message='Password is incorrect correct',
            )
