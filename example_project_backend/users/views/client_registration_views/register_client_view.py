from django.contrib.auth import login
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from common.django_utils.api_checkers.request_data_fields_api_checker import RequestDataFieldsAPIChecker
from operations_tasks.managers.operation_tasks_creator import OperationsTasksCreator
from users.apis_checkers.passwords_repeat_api_checker import PasswordRepeatAPIChecker
from users.managers.client_registration_manager import ClientRegistrationManager


class RegisterClientView(APIView):
    def post(self, request: Request) -> Response:
        RequestDataFieldsAPIChecker(['new_password', 'password_repeat', 'pin', 'first_name', 'last_name',
                                     'organization_name', 'email', 'phone_number'])\
            .raise_exception_if_not_valid(request=request)
        new_password = request.data['new_password']
        password_repeat = request.data['password_repeat']
        PasswordRepeatAPIChecker().raise_exception_if_not_valid(new_password, password_repeat)
        pin = request.data['pin']
        first_name = request.data['first_name']
        last_name = request.data['last_name']
        organization_name = request.data['organization_name']
        email = request.data['email']
        phone_number = request.data['phone_number']
        user = ClientRegistrationManager().register_client(first_name, last_name, organization_name, email,
                                                           phone_number, new_password, pin)
        OperationsTasksCreator.create_new_client_didnt_open_sub_project_task(user)
        login(request, user)
        return Response({}, status=status.HTTP_200_OK)
