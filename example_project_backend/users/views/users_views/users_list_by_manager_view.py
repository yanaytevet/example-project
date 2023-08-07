from typing import Set, Type

from django.db.models import Model, QuerySet
from rest_framework.request import Request

from common.consts.viewer_types import ViewerTypes
from common.django_utils.api_checkers.org_manager_api_checker import OrgManagerAPIChecker
from common.django_utils.api_checkers.request_data_fields_api_checker import RequestDataFieldsAPIChecker
from common.django_utils.rest_utils import BaseAPIListView
from common.django_utils.serializers.serializer import Serializer
from common.type_hints import JSONType
from users.models import User
from users.serializers.short_user_serializer import ShortUserSerializer
from users.users_actions.general_users_actions import GeneralUsersActions


class UsersListByManagerView(BaseAPIListView):

    @classmethod
    def get_model_cls(cls) -> Type[Model]:
        return User

    @classmethod
    def get_item_serializer(cls) -> Serializer:
        return ShortUserSerializer()

    @classmethod
    def get_list_serializer(cls) -> Serializer:
        return ShortUserSerializer()

    @classmethod
    def get_viewer_type(cls, user: User) -> ViewerTypes:
        return ViewerTypes.CLIENT

    @classmethod
    def get_create_allowed_attributes_set(cls) -> Set[str]:
        return {"email", "first_name", "last_name", "new_password", "teams"}

    @classmethod
    def check_permitted_any_request(cls, request: Request, user: User) -> None:
        OrgManagerAPIChecker().raise_exception_if_not_valid(user)

    @classmethod
    def check_permitted_post_request(cls, request: Request, user: User) -> None:
        RequestDataFieldsAPIChecker(["email", "new_password"]).raise_exception_if_not_valid(request)

    @classmethod
    def modify_objects_for_request(cls, request: Request, user: User, objects: QuerySet) -> QuerySet:
        return objects.filter(organization=user.organization).order_by('id')

    @classmethod
    def create_obj_post(cls, user: User, data: JSONType, create_allowed_attributes_set: Set[str]) -> Model:
        email = data['email']
        new_password = data['new_password']
        first_name = data.get('first_name', '')
        last_name = data.get('last_name', '')
        teams_ids = data.get('teams_ids', [])
        new_user = GeneralUsersActions().create_user_by_org_manager(
            email=email, password=new_password, first_name=first_name, last_name=last_name, teams_ids=teams_ids,
            org_manager=user)
        return new_user

