from common.simple_rest.async_api_request import AsyncAPIRequest
from common.simple_rest.async_views.async_simple_post_api_view import AsyncSimplePostAPIView
from common.simple_rest.constants.status_code import StatusCode
from common.simple_rest.exceptions.rest_api_exception import RestAPIException
from common.simple_rest.permissions_checkers.request_data_fields_checker import RequestDataFieldsAPIChecker
from common.type_hints import JSONType
from users.models import User, TemporaryAccess


class ForgotMyPasswordView(AsyncSimplePostAPIView):
    @classmethod
    async def check_permitted(cls, request: AsyncAPIRequest, **kwargs) -> None:
        RequestDataFieldsAPIChecker(['email']).raise_exception_if_not_valid(request=request)

    @classmethod
    async def run_action(cls, request: AsyncAPIRequest, **kwargs) -> JSONType:
        user_obj = await User.async_get_by_username(request.data['email'].lower().replace(' ', ''))
        if not user_obj:
            raise RestAPIException(
                status_code=StatusCode.HTTP_401_UNAUTHORIZED,
                error_code='incorrect_user',
                message='Incorrect user',
            )

        if TemporaryAccess.user_id_already_has(user_obj.id):
            message = f'''Email was already sent in the last {TemporaryAccess.TTL_MINUTES} minutes.
            If it wasn't you or the email didn\'t arrive, please contact our customers  support.'''
            raise RestAPIException(
                status_code=StatusCode.HTTP_403_FORBIDDEN,
                error_code='email_was_already_sent',
                message=message,
            )

        temporary_access = TemporaryAccess.create_for_user(user_obj)
        # send_forgot_my_password_emails_task.delay(temporary_access.id)
        return {}
