from django.contrib.auth import get_user
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from common.django_utils.api_checkers.login_api_checker import LoginAPIChecker
from users.status_manager import StatusDataManager


class MyStatusView(APIView):
    def get(self, request: Request) -> Response:
        user = get_user(request)
        LoginAPIChecker().raise_exception_if_not_valid(user)
        status_data = StatusDataManager(user).get_my_status()

        return Response(status_data, status=status.HTTP_200_OK)
