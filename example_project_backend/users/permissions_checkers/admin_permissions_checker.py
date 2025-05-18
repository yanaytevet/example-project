from common.simple_api.enums.status_code import StatusCode
from common.simple_api.exceptions.rest_api_exception import RestAPIException
from common.simple_api.permissions_checkers.permissions_checker import PermissionsChecker
from users.models import User


class AdminPermissionsChecker(PermissionsChecker):
    async def async_raise_exception_if_not_valid(self, user: User) -> None:
        if not user.is_admin():
            raise RestAPIException(
                status_code=StatusCode.HTTP_403_FORBIDDEN,
                message='User is not an admon.',
                error_code='user_is_not_admin',
            )
