from rest_framework import status
from rest_framework.exceptions import APIException
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from common.django_utils.api_checkers.request_data_fields_api_checker import RequestDataFieldsAPIChecker
from emails.tasks.users_emails_tasks.send_forgot_my_password_emails_task import send_forgot_my_password_emails_task
from users.models import User, TemporaryAccess


class InvalidCurrentPasswordAPIException(APIException):
    status_code = status.HTTP_403_FORBIDDEN
    default_detail = 'Current password is invalid.'
    default_code = 'invalid_current_password'


class ForgotMyPasswordView(APIView):
    def post(self, request: Request) -> Response:
        RequestDataFieldsAPIChecker(['email']).raise_exception_if_not_valid(request=request)
        user_obj = User.get_by_username(request.data['email'].lower().replace(' ', ''))
        if not user_obj:
            raise APIException(detail='Email is incorrect', code=status.HTTP_401_UNAUTHORIZED)

        if TemporaryAccess.user_id_already_has(user_obj.id):
            raise APIException(detail=f'''Email was already sent in the last {TemporaryAccess.TTL_MINUTES} minutes. 
If it wasn't you or the email didn\'t arrive, please contact our customers  support.''', code=status.HTTP_403_FORBIDDEN)

        temporary_access = TemporaryAccess.create_for_user(user_obj)
        send_forgot_my_password_emails_task.delay(temporary_access.id)
        return Response({}, status=status.HTTP_200_OK)
