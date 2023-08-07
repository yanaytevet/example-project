from typing import List

from rest_framework.request import Request

from common.django_utils.api_checkers.org_manager_api_checker import OrgManagerAPIChecker
from common.test_utils.base_urls_test import BaseURLsTest
from users.consts.permissions import Permissions
from users.models import User, Team


class TestMyUsersURLs(BaseURLsTest):
    def setUp(self) -> None:
        super().setUp()
        self.admin_user = self.create_admin()
        self.manager_user = self.create_manager(self.org_1)
        self.client_user = self.create_client(self.org_1, teams=[self.team_1a])
        self.expert_user = self.create_expert()

    def test_my(self) -> None:
        self.client.force_login(self.admin_user)
        self.successful_get_my_user(self.admin_user)
        self.failed_get_my_teams()
        self.failed_get_my_org()
        self.assert_methods_urls_not_allowed()

        self.client.force_login(self.manager_user)
        self.successful_get_my_user(self.manager_user, teams=[self.team_1a, self.team_1b])
        self.successful_get_my_teams([self.team_1a, self.team_1b])
        self.successful_get_my_org()
        self.assert_methods_urls_not_allowed()

        self.client.force_login(self.client_user)
        self.successful_get_my_user(self.client_user, teams=[self.team_1a])
        self.successful_get_my_teams([self.team_1a, self.team_1b])
        self.successful_get_my_org()
        self.assert_methods_urls_not_allowed()

        self.client.force_login(self.expert_user)
        self.successful_get_my_user(self.expert_user)
        self.failed_get_my_teams()
        self.failed_get_my_org()
        self.assert_methods_urls_not_allowed()

    def successful_get_my_user(self, user_obj: User, teams: List[Team] = None) -> None:
        is_client = user_obj.is_client()
        is_expert = user_obj.is_expert()
        is_admin = user_obj.is_superuser or user_obj.is_staff
        is_org_manager = OrgManagerAPIChecker().is_valid(user_obj)
        permissions = [Permissions.ORG_MANAGER] if is_org_manager else []

        organization_json = {
            'id': self.org_1.id,
            'name': self.org_1.name,
            'calls_done_in_subscription': 0,
            'credits_used_in_subscription': 0,
            'max_credits_in_subscription': 100,
            'credits_left_in_subscription': 100,
            'questions_max_amount': 10,
            'can_make_more_calls': True,
            'allow_complex_project_interaction': False,
        } if is_client else None
        teams_json = [{'id': team.id, 'name': team.name} for team in teams] if teams else []

        response = self.get_my_user()
        self.assertEqual(response.status_code, 200)
        self.assert_partially_equal({
            'id': user_obj.id,
            'username': user_obj.username,
            'email': f'{user_obj.username}@xperiti.com',
            'preferred_language': 'en-us',
            'full_name': user_obj.get_full_name(),
            'is_client': is_client,
            'is_expert': is_expert,
            'is_admin': is_admin,
            'pic_url': '',
            'permissions': permissions,
            'is_org_manager': is_org_manager,
            'organization': organization_json,
            'teams': teams_json,
        }, response.json())

    def successful_get_my_teams(self, teams: List[Team]) -> None:
        response = self.get_my_teams()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), [{
            'id': team.id,
            'name': team.name,
        } for team in teams])

    def successful_get_my_org(self) -> None:
        response = self.get_my_org()
        self.assertEqual(response.status_code, 200)
        self.assert_partially_equal({
            'id': self.org_1.id,
            'name': self.org_1.name,
            'teams': [{'id': self.team_1a.id, 'name': 'team_1a'}, {'id': self.team_1b.id, 'name': 'team_1b'}],
            'description': '',
            'logo_url': '',
            'calls_done_in_subscription': 0,
            'credits_used_in_subscription': 0,
            'max_credits_in_subscription': 100,
            'credits_left_in_subscription': 100,
            'total_users_in_subscription': 10,
            'total_projects': 0,
            'users_count': 2,
            'subscription_start_date': None,
            'subscription_end_date': None,
            'allow_project_serial_number': False,
            'allow_internal_search': False,
            'allow_complex_project_interaction': False,
        }, response.json())

    def failed_get_my_org(self) -> None:
        response = self.get_my_org()
        self.assertEqual(401, response.status_code)
        self.assertEqual({'detail': 'Must be client.'}, response.json())

    def failed_get_my_teams(self) -> None:
        response = self.get_my_teams()
        self.assertEqual(401, response.status_code)
        self.assertEqual({'detail': 'Must be client.'}, response.json())

    def assert_methods_urls_not_allowed(self):
        self.assert_post_not_allowed('/api/users/my/')
        self.assert_post_not_allowed('/api/teams/my/')
        self.assert_post_not_allowed('/api/organizations/my/')
        self.assert_put_not_allowed('/api/users/my/')
        self.assert_put_not_allowed('/api/organizations/my/')
        self.assert_delete_not_allowed('/api/users/my/')
        self.assert_delete_not_allowed('/api/teams/my/')
        self.assert_delete_not_allowed('/api/organizations/my/')

    def get_my_user(self) -> Request:
        return self.client.get('/api/users/my/', {}, format='json')

    def get_my_teams(self) -> Request:
        return self.client.get('/api/teams/my/', {}, format='json')

    def get_my_org(self) -> Request:
        return self.client.get('/api/organizations/my/', {}, format='json')
