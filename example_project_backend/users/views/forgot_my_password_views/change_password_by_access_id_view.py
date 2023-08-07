from rest_framework import status
from rest_framework.exceptions import APIException
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from common.django_utils.api_checkers.request_data_fields_api_checker import RequestDataFieldsAPIChecker, \
    RequestQueryParamsAPIChecker
from users.models import TemporaryAccess
from users.serializers.user_serializer import UserSerializer


class InvalidCurrentPasswordAPIException(APIException):
    status_code = status.HTTP_403_FORBIDDEN
    default_detail = 'Current password is invalid.'
    default_code = 'invalid_current_password'


class ChangePasswordByAccessIdView(APIView):
    def get(self, request: Request) -> Response:
        RequestQueryParamsAPIChecker(['user_id', 'access_id']).raise_exception_if_not_valid(request=request)
        try:
            temporary_access = TemporaryAccess.objects.get(
                user_id=request.query_params['user_id'], access_id=request.query_params['access_id'])
        except TemporaryAccess.DoesNotExist as e:
            raise APIException(detail='Access id is incorrect, maybe the link is too old?',
                               code=status.HTTP_401_UNAUTHORIZED)

        data = UserSerializer().serialize(temporary_access.user)
        return Response(data, status=status.HTTP_200_OK)

    def post(self, request: Request) -> Response:
        RequestDataFieldsAPIChecker(['user_id', 'access_id', 'new_password']).raise_exception_if_not_valid(request=request)
        try:
            temporary_access = TemporaryAccess.objects.get(
                user_id=request.data['user_id'], access_id=request.data['access_id'])
        except TemporaryAccess.DoesNotExist as e:
            raise APIException(detail='Access id is incorrect, maybe the link is too old?',
                               code=status.HTTP_401_UNAUTHORIZED)

        user = temporary_access.user
        new_pass = str(request.data["new_password"])
        user.set_password(new_pass)
        user.save()
        temporary_access.delete()

        data = UserSerializer().serialize(temporary_access.user)
        return Response(data, status=status.HTTP_200_OK)
