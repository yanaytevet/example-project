from rest_framework import status
from rest_framework.exceptions import APIException

from users.models import User, Team


class TeamAndUserOrgNotSameOrganizationAPIException(APIException):
    status_code = status.HTTP_403_FORBIDDEN
    default_detail = "User and team do not belong the same organization."
    default_code = "user_and_team_not_same_organization"


class UsersTeamsActions:
    def add_team_to_user(self, user: User, team: Team) -> None:
        if user.organization_id != team.organization_id:
            raise TeamAndUserOrgNotSameOrganizationAPIException()
        user.teams.add(team)

    def add_team_to_user_by_team_id(self, user: User, team_id: int) -> None:
        team = Team.objects.get(id=team_id)
        self.add_team_to_user(user, team)

    def remove_team_from_user(self, user: User, team: Team) -> None:
        user.teams.remove(team)

    def remove_team_from_user_by_team_id(self, user: User, team_id: int) -> None:
        team = Team.objects.get(id=team_id)
        self.remove_team_from_user(user, team)
