from rest_framework import status
from rest_framework.exceptions import APIException
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from common.django_utils.api_checkers.request_data_fields_api_checker import RequestDataFieldsAPIChecker
from common.django_utils.ip_utils import IpUtils
from users.managers.client_registration_manager import ClientRegistrationManager


class ClientRegistrationIsDisabledAPIException(APIException):
    status_code = status.HTTP_401_UNAUTHORIZED
    default_detail = 'We are sorry, client registration is disabled. Please contact customers support.'
    default_code = 'client_registration_is_disabled'


class SendEmailVerificationEmailView(APIView):
    def post(self, request: Request) -> Response:
        raise ClientRegistrationIsDisabledAPIException()
        # ip_address = IpUtils.get_client_ip(request)
        # RequestDataFieldsAPIChecker(['email', 'first_name']).raise_exception_if_not_valid(request=request)
        # email = request.data['email']
        # first_name = request.data['first_name']
        # ClientRegistrationManager().send_email_verification(ip_address, email, first_name)
        # return Response({}, status=status.HTTP_200_OK)
