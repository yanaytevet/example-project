from django.contrib.auth import get_user
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from common.django_utils.api_checkers.login_api_checker import LoginAPIChecker
from users.users_actions.timezone_manager import TimeZoneManager


class MyTimezoneView(APIView):
    def post(self, request: Request) -> Response:
        user = get_user(request)
        if request.session.get('as_other', False):
            return Response({}, status=status.HTTP_200_OK)
        LoginAPIChecker().raise_exception_if_not_valid(user)
        TimeZoneManager(user.person_info).update_by_request(request)
        return Response({}, status=status.HTTP_200_OK)

    def get(self, request: Request) -> Response:
        user = get_user(request)
        LoginAPIChecker().raise_exception_if_not_valid(user)
        timezone = user.get_person_info().preferred_timezone_offset
        return Response({'timezone': timezone}, status=status.HTTP_200_OK)
