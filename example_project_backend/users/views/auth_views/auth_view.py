from django.contrib.auth import get_user, authenticate, login
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from common.django_utils.serializers.serializer_request_data import SerializerRequestData
from common.django_utils.serializers.serializer_request_data_getter import SerializerRequestDataGetter
from configurations.models.auth_key_configurations import AuthKeyConfigurations
from users.serializers.user_serializer import UserSerializer
import jwt


class AuthView(APIView):
    def get(self, request: Request) -> Response:
        data = {
            "is_auth": False,
        }
        user_obj = get_user(request)
        if not self.is_active_user(user_obj) and 'HTTP_AUTHORIZATION' in request.META:
            try:
                token_obj = self.jwt_auth(request)
                user_to_validate = authenticate(request, username=token_obj['email'], password=token_obj['password'])
                login(request, user_to_validate)
                user_obj = get_user(request)
            except jwt.ExpiredSignatureError:
                return Response({'success': False, 'error': 'Token expired'}, status=status.HTTP_401_UNAUTHORIZED)
            except Exception as e:
                return Response({'success': False, 'error': 'Token invalid'}, status=status.HTTP_400_BAD_REQUEST)
        if self.is_active_user(user_obj):
            data["is_auth"] = True
            serializer = UserSerializer()
            serializer.data = SerializerRequestData(
                viewer_type=SerializerRequestDataGetter.get_viewer_type_by_user(user_obj))
            data["user"] = serializer.serialize(user_obj)
        else:
            data["user"] = None
        return Response(data, status=status.HTTP_200_OK)

    def is_active_user(self, user_obj: User) -> bool:
        return user_obj and not user_obj.is_anonymous

    def jwt_auth(self, request: Request) -> dict:
        token = request.META.get('HTTP_AUTHORIZATION', " ").split(' ')[1]
        secret = AuthKeyConfigurations.get().auth_jwt_key
        payload = jwt.decode(token, secret, algorithms=['HS256'])
        return payload
