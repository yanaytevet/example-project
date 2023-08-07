from typing import Set, Type

from django.db.models import Model, QuerySet
from rest_framework.exceptions import MethodNotAllowed
from rest_framework.request import Request

from common.consts.viewer_types import ViewerTypes
from common.django_utils.api_checkers.client_api_checker import ClientAPIChecker
from common.django_utils.rest_utils import BaseAPIListView
from common.django_utils.serializers.serializer import Serializer
from users.models import User
from users.serializers.short_user_serializer import ShortUserSerializer


class UsersListByClientView(BaseAPIListView):

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
        return set()

    @classmethod
    def check_permitted_any_request(cls, request: Request, user: User) -> None:
        ClientAPIChecker().raise_exception_if_not_valid(user)

    @classmethod
    def check_permitted_post_request(cls, request: Request, user: User) -> None:
        raise MethodNotAllowed('POST')

    @classmethod
    def modify_objects_for_request(cls, request: Request, user: User, objects: QuerySet) -> QuerySet:
        return objects.filter(organization=user.organization)
