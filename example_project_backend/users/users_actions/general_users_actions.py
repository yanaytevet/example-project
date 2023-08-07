from typing import List

from rest_framework import status
from rest_framework.exceptions import APIException

from common.time_utils import TimeUtils
from emails.tasks.users_emails_tasks.send_user_created_emails_task import send_user_created_emails_task
from emails.tasks.users_emails_tasks.send_user_password_changed_by_org_manager_emails_task import \
    send_user_password_changed_by_org_manager_emails_task
from operations_tasks.managers.operation_tasks_creator import OperationsTasksCreator
from users.apis_checkers.teams_api_checkers import TeamBelongToOrgAPIChecker
from users.apis_checkers.users_api_checkers import UsernameAlreadyExistAPIException, TooManyUsersAPIException
from users.consts.permissions import Permissions
from users.models import User, Team
from users.users_actions.organization_actions import OrganizationActions


class CantDeleteManagersAPIException(APIException):
    status_code = status.HTTP_403_FORBIDDEN
    default_detail = "Cannot delete managers."
    default_code = "cant_delete_managers"


class GeneralUsersActions:
    def __init__(self, done_by_admin: bool = False):
        self.done_by_admin = done_by_admin

    def delete_user(self, user: User) -> None:
        if not self.done_by_admin and Permissions.ORG_MANAGER in user.permissions_array:
            raise CantDeleteManagersAPIException()
        user.delete()

    def create_user_by_org_manager(self, email: str, password: str, org_manager: User, first_name: str = '',
                                   last_name: str = '', teams_ids: List[int] = None) -> User:
        organization = org_manager.organization
        if organization.user_set.count() >= organization.total_users_in_subscription:
            raise TooManyUsersAPIException(organization.total_users_in_subscription)
        if User.get_by_username(email):
            raise UsernameAlreadyExistAPIException()

        new_user = User(username=email, email=email)
        person_info = new_user.get_person_info()
        person_info.first_name = first_name
        person_info.last_name = last_name
        new_user.set_password(password)
        new_user.organization = organization
        new_user.save()

        for team_id in teams_ids:
            team = Team.objects.get(id=team_id)
            TeamBelongToOrgAPIChecker().raise_exception_if_not_valid(team, organization)
            new_user.teams.add(team)
        send_user_created_emails_task.delay(new_user.id, org_manager.id)
        OperationsTasksCreator.create_new_client_didnt_open_sub_project_task(new_user)
        return new_user

    def change_password_by_org_manager(self, user: User, org_manager: User, password: str) -> None:
        user.set_password(password)
        user.save()
        send_user_password_changed_by_org_manager_emails_task.delay(user.id, org_manager.id)

    def change_password_by_admin(self, user: User, admin: User, password: str) -> None:
        user.set_password(password)
        user.save()

    def update_last_call_created_time(self, user: User) -> None:
        user.last_call_created_time = TimeUtils.now()
        user.save()
        OrganizationActions(user.organization).update_last_call_created_time()

    def update_last_sub_project_created_time(self, user: User) -> None:
        user.last_sub_project_created_time = TimeUtils.now()
        user.save()
        OrganizationActions(user.organization).update_last_sub_project_created_time()
