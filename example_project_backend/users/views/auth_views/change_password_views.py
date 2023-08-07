from django.contrib.auth import authenticate, get_user
from rest_framework import status
from rest_framework.exceptions import APIException
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from common.django_utils.api_checkers.login_api_checker import LoginAPIChecker
from common.django_utils.api_checkers.request_data_fields_api_checker import RequestDataFieldsAPIChecker
from users.models import UserEvent


class InvalidCurrentPasswordAPIException(APIException):
    status_code = status.HTTP_403_FORBIDDEN
    default_detail = 'Current password is invalid.'
    default_code = 'invalid_current_password'


class ChangePasswordView(APIView):
    def post(self, request: Request) -> Response:
        user_obj = get_user(request)

        RequestDataFieldsAPIChecker(['old_password', 'new_password']).raise_exception_if_not_valid(request=request)
        LoginAPIChecker().raise_exception_if_not_valid(user_obj)

        old_pass = str(request.data["old_password"])
        user = authenticate(request, username=user_obj.username, password=old_pass)

        if user:
            new_pass = str(request.data["new_password"])
            user.set_password(new_pass)
            user.save()
            UserEvent(name='change_my_password', user=user).save()
            return Response({"is_success": True, "msg": "Password successfully changed"},
                            status=status.HTTP_200_OK)

        else:
            raise InvalidCurrentPasswordAPIException()
