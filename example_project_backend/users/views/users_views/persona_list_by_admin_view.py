from typing import Set, Type

from django.db.models import Model, QuerySet
from rest_framework.exceptions import MethodNotAllowed
from rest_framework.request import Request

from common.consts.viewer_types import ViewerTypes
from common.django_utils.api_checkers.admin_api_checker import AdminAPIChecker
from common.django_utils.api_checkers.login_api_checker import LoginAPIChecker
from common.django_utils.rest_utils import BaseAPIItemView, BaseAPIListView
from common.django_utils.serializers.serializer import Serializer
from users.models import User
from users.serializers.persona_serializer import PersonaSerializer
from users.models.persona import Persona



class PersonaListByAdminView(BaseAPIListView):

    @classmethod
    def get_model_cls(cls) -> Type[Model]:
        return Persona

    @classmethod
    def get_item_serializer(cls) -> Serializer:
        return PersonaSerializer()

    @classmethod
    def get_list_serializer(cls) -> Serializer:
        return PersonaSerializer()

    @classmethod
    def get_viewer_type(cls, user: User) -> ViewerTypes:
        return ViewerTypes.ADMIN

    @classmethod
    def get_create_allowed_attributes_set(cls) -> Set[str]:
        return set()

    @classmethod
    def check_permitted_any_request(cls, request: Request, user: User) -> None:
        AdminAPIChecker().raise_exception_if_not_valid(user)
