from typing import Type

from ninja import Schema, Path

from common.simple_api.api_request import APIRequest
from common.simple_api.enums.status_code import StatusCode
from common.simple_api.exceptions.rest_api_exception import RestAPIException
from common.simple_api.permissions_checkers.login_permission_checker import LoginPermissionChecker
from common.simple_api.views.simple_post_api_view import SimplePostAPIView
from users.managers.django_auth import DjangoAuth


class ChangePasswordInputSchema(Schema):
    old_password: str
    new_password: str


class ChangePasswordOutputSchema(Schema):
    is_success: bool
    msg: str


class ChangePasswordView(SimplePostAPIView):
    @classmethod
    def get_output_schema(cls) -> Type[Schema]:
        return ChangePasswordOutputSchema

    @classmethod
    def get_data_schema(cls) -> Type[Schema]:
        return ChangePasswordInputSchema

    @classmethod
    async def check_permitted(cls, request: APIRequest, data: ChangePasswordInputSchema, path: Path = None) -> None:
        user_obj = await request.future_user
        await LoginPermissionChecker().async_raise_exception_if_not_valid(user_obj)

    @classmethod
    async def run_action(cls, request: APIRequest, data: ChangePasswordInputSchema, path: Path = None
                         ) -> ChangePasswordOutputSchema:
        user_obj = await request.future_user

        await LoginPermissionChecker().async_raise_exception_if_not_valid(user_obj)

        old_pass = str(data.old_password)
        user = await DjangoAuth.async_authenticate(request, username=user_obj.username, password=old_pass)

        if user:
            new_pass = str(data.new_password)
            user.set_password(new_pass)
            await user.asave()
            return ChangePasswordOutputSchema(is_success=True, msg='Password successfully changed')

        else:
            raise RestAPIException(
                status_code=StatusCode.HTTP_401_UNAUTHORIZED,
                error_code='password_is_incorrect_correct',
                message='Password is incorrect correct',
            )
