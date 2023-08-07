from typing import Set, Type

from django.db.models import Model
from rest_framework.request import Request

from common.consts.viewer_types import ViewerTypes
from common.django_utils.api_checkers.admin_api_checker import AdminAPIChecker
from common.django_utils.api_checkers.request_data_fields_api_checker import RequestDataFieldsAPIChecker
from common.django_utils.rest_utils import BaseAPIListView
from common.django_utils.serializers.serializer import Serializer
from common.time_utils import TimeUtils
from users.consts.permissions import Permissions
from users.models import User, Organization
from users.serializers.short_organization_for_admin_serializer import ShortOrganizationForAdminSerializer
from users.users_actions.users_permissions_actions import UsersPermissionsActions


class OrganizationsListByAdminView(BaseAPIListView):

    @classmethod
    def get_model_cls(cls) -> Type[Model]:
        return Organization

    @classmethod
    def get_item_serializer(cls) -> Serializer:
        return ShortOrganizationForAdminSerializer()

    @classmethod
    def get_list_serializer(cls) -> Serializer:
        return ShortOrganizationForAdminSerializer()

    @classmethod
    def get_viewer_type(cls, user: User) -> ViewerTypes:
        return ViewerTypes.ADMIN

    @classmethod
    def get_create_allowed_attributes_set(cls) -> Set[str]:
        return {"name", "description", "max_credits_in_subscription", "total_users_in_subscription"}

    @classmethod
    def run_after_post(cls, request: Request, user: User, obj: Organization) -> None:
        obj.subscription_start_date = TimeUtils.now()
        obj.subscription_end_date = TimeUtils.add_years_to_time(obj.subscription_start_date, 1)
        obj.save()

        org_manager_username = request.data.get('org_manager_username')
        org_manager_password = request.data.get('org_manager_password')
        if org_manager_username and org_manager_password:
            org_manager_username = org_manager_username.lower()
            user: User = User.objects.create_user(org_manager_username, email=org_manager_username,
                                                  password=org_manager_password, organization=obj)
            user.set_primary_email(org_manager_username)
            user.save()
            user.refresh_from_db()
            UsersPermissionsActions().add_permission_to_user(user, Permissions.ORG_MANAGER)

    @classmethod
    def check_permitted_any_request(cls, request: Request, user: User) -> None:
        AdminAPIChecker().raise_exception_if_not_valid(user)

    @classmethod
    def check_permitted_post_request(cls, request: Request, user: User) -> None:
        RequestDataFieldsAPIChecker(["name"]).raise_exception_if_not_valid(request)
