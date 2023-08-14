from common.django_utils.django_auth import DjangoAuth
from common.simple_rest.async_api_request import AsyncAPIRequest
from common.simple_rest.async_views.async_simple_post_api_view import AsyncSimplePostAPIView
from common.simple_rest.permissions_checkers.login_permission_checker import LoginPermissionChecker
from common.type_hints import JSONType


class LogoutView(AsyncSimplePostAPIView):
    @classmethod
    async def check_permitted(cls, request: AsyncAPIRequest, **kwargs) -> None:
        await LoginPermissionChecker().async_raise_exception_if_not_valid(request)

    @classmethod
    async def run_action(cls, request: AsyncAPIRequest, **kwargs) -> JSONType:
        await DjangoAuth.async_logout(request)
        return {'is_auth': False, 'user': None}
