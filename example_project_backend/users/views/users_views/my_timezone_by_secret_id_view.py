from django.contrib.auth import get_user
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from common.django_utils.api_checkers.login_api_checker import LoginAPIChecker
from experts.apis_checkers.experts_api_checkers import ExpertSecretIdAPIChecker
from experts.models import Expert
from users.users_actions.timezone_manager import TimeZoneManager


class MyTimezoneBySecretIdView(APIView):
    def post(self, request: Request, expert_id: int) -> Response:
        obj = Expert.objects.get(id=expert_id)
        user = get_user(request)
        if LoginAPIChecker().is_valid(user):
            return Response({}, status=status.HTTP_200_OK)
        ExpertSecretIdAPIChecker().raise_exception_if_not_valid(obj, request.data['secret_id'])
        TimeZoneManager(obj.person_info).update_by_request(request)
        return Response({}, status=status.HTTP_200_OK)

