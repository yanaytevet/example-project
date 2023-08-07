from rest_framework import status
from rest_framework.exceptions import APIException

from users.consts.permissions import Permissions
from users.models import User, Organization


class NoManagersLeftAPIException(APIException):
    status_code = status.HTTP_403_FORBIDDEN
    default_detail = "There are no other managers, aborted."
    default_code = "no_managers_left"


class UsersPermissionsActions:
    def __init__(self, done_by_admin: bool = False):
        self.done_by_admin = done_by_admin

    def add_permission_to_user(self, user: User, permission: Permissions) -> None:
        user.permissions_array.append(permission)
        user.save()

    def remove_permission_from_user(self, user: User, permission: Permissions) -> None:
        if not self.done_by_admin and permission == Permissions.ORG_MANAGER:
            self.check_there_are_more_managers(user.organization)
        user.permissions_array.remove(permission)
        user.save()

    def check_there_are_more_managers(self, organization: Organization) -> None:
        if User.objects.filter(organization=organization, permissions_array__contains=[Permissions.ORG_MANAGER]).count() <= 1:
            raise NoManagersLeftAPIException()
