from typing import Set, Type, Optional

from django.db.models import Model, QuerySet
from rest_framework.request import Request

from common.consts.viewer_types import ViewerTypes
from common.django_utils.api_checkers.admin_api_checker import AdminAPIChecker
from common.django_utils.rest_utils import BaseAPIListView
from common.django_utils.serializers.serializer import Serializer
from common.type_hints import JSONType
from users.models import User, Organization
from users.serializers.table_user_serializer import TableUserSerializer


class UsersListByAdminView(BaseAPIListView):

    @classmethod
    def get_model_cls(cls) -> Type[Model]:
        return User

    @classmethod
    def get_item_serializer(cls) -> Serializer:
        return TableUserSerializer()

    @classmethod
    def get_list_serializer(cls) -> Serializer:
        return TableUserSerializer()

    @classmethod
    def get_viewer_type(cls, user: User) -> ViewerTypes:
        return ViewerTypes.ADMIN

    @classmethod
    def get_create_allowed_attributes_set(cls) -> Set[str]:
        return set()

    @classmethod
    def check_permitted_any_request(cls, request: Request, user: User) -> None:
        AdminAPIChecker().raise_exception_if_not_valid(user)

    @classmethod
    def modify_objects_for_request(cls, request: Request, user: User, objects: QuerySet) -> QuerySet:
        organization_id = request.query_params.get('organization_id')
        if organization_id:
            objects = objects.filter(organization_id=int(organization_id))
        return objects.order_by('id')

    @classmethod
    def create_obj_post(cls, user: User, data: JSONType, create_allowed_attributes_set: Set[str]) -> Optional[User]:
        email = data['email'].lower()
        password = data['new_password']
        organization_id = data['organization_id']
        first_name = data['first_name']
        last_name = data['last_name']
        organization = Organization.objects.get(id=organization_id)
        username = email.lower()
        new_user: User = User.objects.create_user(username, email=email, password=password, organization=organization)
        new_user.set_primary_email(email)
        new_user.save()
        new_user.refresh_from_db()
        new_user.person_first_name = first_name
        new_user.person_last_name = last_name
        new_user.save()
        return new_user
