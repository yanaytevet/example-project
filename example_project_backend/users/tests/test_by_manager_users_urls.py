from typing import List

from rest_framework import status
from rest_framework.request import Request

from common.test_utils.base_urls_test import BaseURLsTest
from common.type_hints import JSONType
from users.models import User, Team


class TestByManagerUsersURLs(BaseURLsTest):
    def setUp(self) -> None:
        super().setUp()
        self.admin_user = self.create_admin()
        self.manager_1_user = self.create_manager(self.org_1)
        self.client_1a_user = self.create_client(self.org_1, teams=[self.team_1a])
        self.manager_2_user = self.create_manager(self.org_2)
        self.client_2a_user = self.create_client(self.org_2, teams=[self.team_2a])
        self.expert_user = self.create_expert()

    def test_by_manager(self) -> None:
        self.client.force_login(self.admin_user)
        self.failed_all_actions()

        self.client.force_login(self.manager_1_user)
        self.successful_get_users_by_manager([self.manager_1_user, self.client_1a_user])
        self.client_1b_user = self.successful_create_user_by_manager()
        self.successful_get_users_by_manager([self.manager_1_user, self.client_1a_user, self.client_1b_user])
        # self.successful_get_user_by_manager(self.client_1a_user)
        # self.successful_put_update_user_by_manager(self.client_1b_user)
        # self.successful_put_add_manager_user_by_manager(self.client_1b_user)
        # self.successful_put_remove_manager_user_by_manager(self.client_1b_user)
        # self.successful_put_add_team_user_by_manager(self.client_1b_user, self.team_1b)
        # self.successful_delete_user_by_manager(self.client_1a_user)
        # self.successful_get_users_by_manager([self.manager_1_user, self.client_1b_user])
        # self.failed_get_user_by_manager(self.client_2a_user)
        # self.failed_put_user_by_manager(self.client_2a_user)
        # self.failed_delete_user_by_manager(self.client_2a_user)
        # self.failed_put_remove_manager_user_by_manager(self.manager_1_user)
        # self.failed_put_remove_manager_user_by_manager(self.manager_2_user)
        #
        # self.successful_get_teams_by_manager([self.team_1a, self.team_1b])
        # self.team_1c = self.successful_create_team_by_manager()
        # self.successful_get_teams_by_manager([self.team_1a, self.team_1b, self.team_1c])
        # self.successful_get_team_by_manager(self.team_1a)
        # self.successful_put_team_by_manager(self.team_1a)
        # self.failed_delete_team_by_manager(self.team_1b)
        # self.failed_get_team_by_manager(self.team_2a)
        # self.failed_put_team_by_manager(self.team_2a)
        # self.failed_delete_team_by_manager(self.team_2b)

        self.client.force_login(self.client_1a_user)
        self.failed_all_actions()

    def failed_all_actions(self) -> None:
        self.failed_get_users_by_manager()
        self.failed_create_user_by_manager()
        # self.failed_get_user_by_manager(self.client_1a_user)
        # self.failed_put_user_by_manager(self.client_1a_user)
        # self.failed_delete_user_by_manager(self.client_1a_user)

        # self.failed_get_teams_by_manager()
        # self.failed_create_team_by_manager()
        # self.failed_get_team_by_manager(self.team_2a)
        # self.failed_put_team_by_manager(self.team_1a)
        # self.failed_delete_team_by_manager(self.team_1b)

    def successful_get_users_by_manager(self, users: List[User]) -> None:
        resp = self.get_users_by_manager()
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assert_partially_equal([
            {
                'id': user.id,
                'username': user.username,
                'email': user.get_primary_email(),
                'full_name': user.get_full_name(),
            } for user in users
        ], resp.json())

    def failed_get_users_by_manager(self) -> None:
        resp = self.get_users_by_manager()
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(resp.json(), {'detail': 'Missing permissions org_manager'})

    def get_users_by_manager(self) -> Request:
        return self.client.get('/api/users/by-manager/', {}, format='json')

    def successful_create_user_by_manager(self) -> User:
        resp = self.create_user_by_manager({'email': f'email{self.users_count}@gmail.com',
                                            'new_password': 'ghfh56fds3s'})
        self.users_count += 1
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

        user = User.objects.last()

        self.assert_partially_equal(
            {
                'id': user.id,
                'username': user.username,
                'email': user.get_primary_email_for_sending().address,
                'full_name': user.get_full_name(),
            }, resp.json())

        return user

    def failed_create_user_by_manager(self) -> None:
        resp = self.create_user_by_manager({})
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(resp.json(), {'detail': 'Missing permissions org_manager'})

    def create_user_by_manager(self, data: JSONType) -> Request:
        return self.client.post('/api/users/by-manager/', data, format='json')
