from rest_framework.request import Request

from users.consts.permissions import Permissions
from users.models import User
from users.users_actions.general_users_actions import GeneralUsersActions
from users.users_actions.users_permissions_actions import UsersPermissionsActions
from users.users_actions.users_teams_actions import UsersTeamsActions


class UserItemMixin:
    @classmethod
    def delete_obj(cls, obj: User) -> None:
        GeneralUsersActions().delete_user(obj)

    def put_add_team(self, request: Request, user: User, obj: User) -> None:
        team_id = request.data['team_id']
        UsersTeamsActions().add_team_to_user_by_team_id(obj, team_id)

    def put_remove_team(self, request: Request, user: User, obj: User) -> None:
        team_id = request.data['team_id']
        UsersTeamsActions().remove_team_from_user_by_team_id(obj, team_id)

    def put_make_org_manager(self, request: Request, user: User, obj: User) -> None:
        UsersPermissionsActions().add_permission_to_user(obj, Permissions.ORG_MANAGER)

    def put_remove_org_manager(self, request: Request, user: User, obj: User) -> None:
        UsersPermissionsActions().remove_permission_from_user(obj, Permissions.ORG_MANAGER)
