from django.contrib.auth import get_user
from rest_framework import status
from rest_framework.exceptions import APIException
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from common.django_utils.api_checkers.admin_api_checker import AdminAPIChecker
from users.models import User
from users.serializers.user.user_serializer import ShortUserSerializer


class UsernameDoesntExistAPIException(APIException):
    status_code = status.HTTP_404_NOT_FOUND
    default_detail = 'Username doesnt exist'
    default_code = 'username_doesnt_exist'


class UserItemByUsernameByAdminView(APIView):
    def post(self, request: Request, *args, **kwargs) -> Response:
        user = get_user(request)
        AdminAPIChecker().raise_exception_if_not_valid(user)
        objects = User.objects.filter(username=request.data['username'])
        if not objects.count():
            raise UsernameDoesntExistAPIException()
        obj = objects.first()
        data = ShortUserSerializer().serialize(obj)
        return Response(data, status=status.HTTP_200_OK)
