from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from common.django_utils.api_checkers.request_data_fields_api_checker import RequestDataFieldsAPIChecker
from users.managers.client_registration_manager import ClientRegistrationManager


class VerifyEmailByPinView(APIView):
    def post(self, request: Request) -> Response:
        RequestDataFieldsAPIChecker(['email', 'pin']).raise_exception_if_not_valid(request=request)
        email = request.data['email']
        pin = request.data['pin']
        verified = ClientRegistrationManager().check_for_email_verification(email, pin)
        return Response(verified, status=status.HTTP_200_OK)
