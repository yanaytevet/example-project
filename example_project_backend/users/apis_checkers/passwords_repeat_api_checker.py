from common.simple_rest.constants.status_code import StatusCode
from common.simple_rest.exceptions.rest_api_exception import RestAPIException
from common.simple_rest.permissions_checkers.permissions_checker import PermissionsChecker


class PasswordRepeatAPIChecker(PermissionsChecker):
    def raise_exception_if_not_valid(self, password: str, password_repeat: str) -> None:
        if password != password_repeat:
            raise RestAPIException(
                status_code=StatusCode.HTTP_400_BAD_REQUEST,
                message='Passwords are not the same.',
                error_code='passwords_are_not_the_same',
            )
