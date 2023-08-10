from common.simple_rest.async_api_request import AsyncAPIRequest
from common.simple_rest.async_views.async_simple_post_api_view import AsyncSimplePostAPIView
from common.simple_rest.constants.status_code import StatusCode
from common.simple_rest.exceptions.rest_api_exception import RestAPIException
from common.simple_rest.permissions_checkers.request_data_fields_checker import RequestDataFieldsAPIChecker
from common.type_hints import JSONType
from users.models import TemporaryAccess
from users.serializers.user.user_serializer import UserSerializer


class ChangePasswordByAccessIdView(AsyncSimplePostAPIView):
    @classmethod
    async def check_permitted(cls, request: AsyncAPIRequest, **kwargs) -> None:
        await RequestDataFieldsAPIChecker(['user_id', 'access_id', 'new_password']).async_raise_exception_if_not_valid(
            request=request)

    @classmethod
    async def run_action(cls, request: AsyncAPIRequest, **kwargs) -> JSONType:
        try:
            temporary_access = await TemporaryAccess.objects.filter(
                user_id=request.query_params['user_id'], access_id=request.query_params['access_id']).afirst()
        except TemporaryAccess.DoesNotExist as e:
            raise RestAPIException(
                status_code=StatusCode.HTTP_401_UNAUTHORIZED,
                error_code='access_id_is_incorrect',
                message='Access id is incorrect, maybe the link is too old?',
            )

        user = temporary_access.user
        new_pass = str(request.data['new_password'])
        user.set_password(new_pass)
        await user.asave()
        await temporary_access.adelete()

        return UserSerializer().serialize(temporary_access.user)
