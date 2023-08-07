from requests import Response
from rest_framework.request import Request

from common.test_utils.base_urls_test import BaseURLsTest
from common.type_hints import JSONType
from experts.consts.experts_status import ExpertStatus
from experts.models import Expert
from users.models import User, Organization


class TestLogin(BaseURLsTest):
    ADMIN_USER_USERNAME = 'user_admin'
    ADMIN_USER_PASS = 'secret_admin'

    USER1_USERNAME = 'user1'
    USER1_PASS = 'secret1'

    USER2_USERNAME = 'user2'
    USER2_PASS = 'secret2'

    NOUSER_USERNAME = 'user3'
    NOUSER_PASS = 'secret3'

    def setUp(self) -> None:
        super().setUp()
        self.username_to_user_obj = {}

        self.org = Organization(name='test_org')
        self.org.save()

        self.expert = Expert()
        self.expert.set_primary_email('charles@xperiti.com')
        self.expert.person_first_name = "ex"
        self.expert.person_last_name = "pert"
        self.expert.status = ExpertStatus.ACTIVE
        self.expert.save()

        username = self.ADMIN_USER_USERNAME
        self.username_to_user_obj[username] = User.objects.create_user(
            username=username, email=f'{username}@xperiti.com', password=self.ADMIN_USER_PASS, is_superuser=True)

        username = self.USER1_USERNAME
        self.username_to_user_obj[username] = User.objects.create_user(
            username=username, email=f'{username}@xperiti.com', password=self.USER1_PASS, is_superuser=False,
            organization=self.org)

        username = self.USER2_USERNAME
        self.username_to_user_obj[username] = User.objects.create_user(
            username=username, email=f'{username}@xperiti.com', password=self.USER2_PASS, is_superuser=False)

        self.expert.user = self.username_to_user_obj[username]
        self.expert.save()

    def test_login_as_self(self) -> None:
        self.successful_login_flow_as_self(self.ADMIN_USER_USERNAME, self.ADMIN_USER_PASS, False, False, True, False)
        self.successful_login_flow_as_self(self.USER1_USERNAME, self.USER1_PASS, True, False, False, False)
        self.successful_login_flow_as_self(self.USER2_USERNAME, self.USER2_PASS, False, True, False, False)

        self.successful_logout()

        self.failed_login_flow_as_self(self.NOUSER_USERNAME, self.NOUSER_PASS)
        self.failed_login_flow_as_self(self.USER1_USERNAME, self.NOUSER_PASS)
        self.failed_login_flow_as_self(self.ADMIN_USER_USERNAME, self.USER1_PASS)
        self.failed_login_flow_as_self(self.USER1_USERNAME, self.ADMIN_USER_PASS)

    def test_login_as_other(self) -> None:
        self.successful_login_flow_as_other(self.ADMIN_USER_USERNAME, self.ADMIN_USER_PASS, self.ADMIN_USER_USERNAME,
                                            False, False, True, False)
        self.successful_login_flow_as_other(self.ADMIN_USER_USERNAME, self.ADMIN_USER_PASS, self.USER1_USERNAME,
                                            True, False, False, False)
        self.successful_login_flow_as_other(self.ADMIN_USER_USERNAME, self.ADMIN_USER_PASS, self.USER2_USERNAME,
                                            False, True, False, False)

        self.failed_login_flow_as_other(self.NOUSER_USERNAME, self.NOUSER_PASS, self.ADMIN_USER_USERNAME)
        self.failed_login_flow_as_other(self.ADMIN_USER_USERNAME, self.ADMIN_USER_PASS, self.NOUSER_USERNAME)
        self.failed_login_flow_as_other(self.USER1_USERNAME, self.USER1_PASS, self.USER2_USERNAME)
        self.failed_login_flow_as_other(self.USER1_USERNAME, self.USER1_PASS, self.USER1_USERNAME)
        self.failed_login_flow_as_other(self.USER1_USERNAME, self.USER1_PASS, self.NOUSER_USERNAME)
        self.failed_login_flow_as_other(self.USER1_USERNAME, self.USER1_PASS, self.ADMIN_USER_USERNAME)

    def test_change_password(self) -> None:
        pass1 = 'change_pass_1'
        pass2 = 'change_pass_2'
        username = 'change_username'

        user_obj = User.objects.create_user(username=username, email=f'{username}@xperiti.com', password=pass1,
                                                           is_superuser=False)
        self.username_to_user_obj[username] = user_obj

        self.failed_try_change_password_not_logged_in(pass1, pass2)

        self.try_login(username, pass1)
        self.failed_try_change_password_wrong_old_password(self.NOUSER_PASS, pass2)
        self.successful_change_password(pass1, pass2)
        self.successful_logout()

        self.username_to_user_obj[username] = User.objects.get(username=username)
        self.successful_login_flow_as_self(username, pass2, False, False, False, False)

    def successful_login_flow_as_self(self, username: str, password: str, is_client: bool, is_expert: bool,
                                      is_admin: bool, is_org_manager: bool) -> None:
        response = self.try_login(username, password)
        self.assertEqual(response.status_code, 200)
        user_obj = self.username_to_user_obj[username]
        self.assertEqual(int(self.client.session['_auth_user_id']), user_obj.id)
        self.client.force_login(user_obj)

        organization_json = {
            'id': self.org.id,
            'name': self.org.name,
            'credits_used_in_subscription': 0,
            'calls_done_in_subscription': 0,
            'max_credits_in_subscription': 0,
            'credits_left_in_subscription': 0,
            'questions_max_amount': 10,
            'can_make_more_calls': False,
        } if is_client else None

        self.assert_partially_equal({
            'is_auth': True,
            'user': {
                'id': user_obj.id,
                'username': user_obj.username,
                'email': f'{user_obj.username}@xperiti.com',
                'full_name': ' ',
                'teams': [],
                'is_client': is_client,
                'is_expert': is_expert,
                'is_admin': is_admin,
                'is_org_manager': is_org_manager,
                'permissions': [],
                'preferred_language': 'en-us',
                'organization': organization_json,
            }
        }, self.get_user_by_url())

        org_response = self.get_my_org_by_url()
        org_data = org_response.json()
        if is_client:
            self.assertEqual(org_response.status_code, 200)
            self.assert_partially_equal({
                'id': self.org.id,
                'name': self.org.name,
                'description': '',
                'logo_url': '',
                'calls_done_in_subscription': 0,
                'credits_used_in_subscription': 0,
                'max_credits_in_subscription': 0,
                'credits_left_in_subscription': 0,
                'total_users_in_subscription': 10,
                'subscription_start_date': None,
                'subscription_end_date': None,
                'users_count': 1,
                'total_projects': 0,
                'teams': [],
                'allow_project_serial_number': False,
                'allow_internal_search': False,
            }, org_data)
        else:
            self.assertEqual(org_data, {'detail': 'Must be client.'})

        self.successful_logout()

    def successful_login_flow_as_other(self, username: str, password: str, other_username: str, is_client: bool,
                                       is_expert: bool, is_admin: bool, is_org_manager: bool) -> None:
        response = self.try_login_as_other(username, password, other_username)
        self.assertEqual(response.status_code, 200)
        resp_json = response.json()
        self.assertTrue(resp_json['is_auth'])
        user_obj = self.username_to_user_obj[other_username]
        self.assertEqual(int(self.client.session['_auth_user_id']), user_obj.id)
        self.client.force_login(user_obj)

        organization_json = {
            'id': self.org.id,
            'name': self.org.name,
            'credits_used_in_subscription': 0,
            'calls_done_in_subscription': 0,
            'max_credits_in_subscription': 0,
            'credits_left_in_subscription': 0,
            'questions_max_amount': 10,
            'can_make_more_calls': False,
        } if is_client else None

        self.assert_partially_equal({
            'is_auth': True,
            'user': {
                'id': user_obj.id,
                'username': user_obj.username,
                'email': f'{user_obj.username}@xperiti.com',
                'preferred_language': 'en-us',
                'full_name': ' ',
                'teams': [],
                'is_client': is_client,
                'is_expert': is_expert,
                'is_admin': is_admin,
                'is_org_manager': is_org_manager,
                'permissions': [],
                'organization': organization_json,
            }
        }, self.get_user_by_url())

        self.successful_logout()

    def successful_logout(self) -> None:
        response = self.try_logout()
        self.assertEqual(response.status_code, 200)

    def failed_login_flow_as_self(self, username: str, password: str) -> None:
        response = self.try_login(username, password)
        self.assertEqual(401, response.status_code)
        self.assertEqual({'detail': 'Failed to login, Invalid user'}, response.json())

    def failed_login_flow_as_other(self, username: str, password: str, other_username: str) -> None:
        response = self.try_login_as_other(username, password, other_username)
        self.assertEqual(401, response.status_code)
        self.assertEqual({'detail': 'Failed to login, Invalid user'}, response.json())

    def successful_change_password(self, old_password: str, new_password: str) -> None:
        response = self.try_change_password(old_password, new_password)
        self.assertEqual(response.status_code, 200)
        self.assertEqual({'is_success': True, 'msg': 'Password successfully changed'}, response.json())

    def failed_try_change_password_not_logged_in(self, old_password: str, new_password: str) -> None:
        response = self.try_change_password(old_password, new_password)
        self.assertEqual(401, response.status_code)

    def failed_try_change_password_wrong_old_password(self, old_password: str, new_password: str) -> None:
        response = self.try_change_password(old_password, new_password)
        self.assertEqual(403, response.status_code)

    def try_login(self, username: str, password: str) -> Request:
        return self.client.post('/auth/login/', {
            'username': username,
            'password': password,
        }, format='json')

    def try_change_password(self, old_password: str, new_password: str) -> Response:
        return self.client.post('/auth/change-password/', {
            'old_password': old_password,
            'new_password': new_password,
        }, format='json')

    def try_login_as_other(self, username: str, password: str, other_username: str) -> Request:
        return self.client.post('/auth/login/', {
            'username': f'{username}///{other_username}',
            'password': password,
        }, format='json')

    def try_logout(self) -> Request:
        return self.client.post('/auth/logout/', {}, format='json')

    def get_user_by_url(self) -> JSONType:
        return self.client.get('/auth/', {}, format='json').json()

    def get_my_org_by_url(self) -> Request:
        return self.client.get('/api/organizations/my/', {}, format='json')
