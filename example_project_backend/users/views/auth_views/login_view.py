from django.contrib.auth import authenticate, login, logout
from rest_framework import status
from rest_framework.exceptions import APIException, AuthenticationFailed
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from common.django_utils.permissions_utils import check_user_is_admin
from users.models import User
from users.serializers.user_serializer import UserSerializer


class LoginView(APIView):
    def post(self, request: Request) -> Response:
        raw_username = str(request.data['username']).lower().replace(' ', '')
        password = str(request.data['password'])
        if "///" in raw_username:
            return self.authenticate_as_other(request, raw_username, password)
        else:
            return self.authenticate_as_self(request, raw_username, password, request.data['login_type'])

    def authenticate_as_self(self, request: Request, username: str, password: str, login_type:str) -> Response:
        user = authenticate(request, username=username, password=password)

        if user is None:
            raise AuthenticationFailed(detail='Failed to login, Invalid user', code=status.HTTP_401_UNAUTHORIZED)

        if user and not user.is_anonymous:
            login(request, user)
            request.session['as_other'] = False
            data = {"is_auth": True, "msg": "", "user": UserSerializer().serialize(user)}
            if login_type == "CLIENT" and user.is_expert():
                data["msg"] = "EXPERT"
                data["is_auth"] = True
            if login_type == "EXPERT" and not user.is_expert():
                data["msg"] = "CLIENT"
                data["is_auth"] = True
            data["msg"] = login_type if data["msg"] == "" else data["msg"]
            return Response(data, status=status.HTTP_200_OK)
        else:
            raise AuthenticationFailed(detail='Invalid user', code=status.HTTP_401_UNAUTHORIZED)

    def authenticate_as_other(self, request: Request, raw_username: str, password: str) -> Response:
        admin_username, other_username = raw_username.split("///", 2)
        admin_user = authenticate(request, username=admin_username, password=password)

        if admin_user is None:
            raise AuthenticationFailed(detail='Failed to login, Invalid user', code=status.HTTP_401_UNAUTHORIZED)

        if not check_user_is_admin(admin_user):
            raise AuthenticationFailed(detail='Failed to login, Invalid user', code=status.HTTP_401_UNAUTHORIZED)

        other_user = User.get_by_username(other_username)
        if other_user is None:
            raise AuthenticationFailed(detail='Failed to login, Invalid user', code=status.HTTP_401_UNAUTHORIZED)

        login(request, other_user)
        request.session['as_other'] = True
        data = {"is_auth": True, "msg": "", "user": UserSerializer().serialize(other_user)}
        return Response(data, status=status.HTTP_200_OK)
