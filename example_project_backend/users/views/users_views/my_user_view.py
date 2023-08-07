from typing import Set

from django.db.models import Model
from rest_framework.exceptions import MethodNotAllowed
from rest_framework.request import Request

from common.django_utils.api_checkers.login_api_checker import LoginAPIChecker
from common.django_utils.rest_utils import BaseAPIItemView
from common.django_utils.serializers.serializer import Serializer
from users.models import User
from users.serializers.user_serializer import UserSerializer


class MyUserItemView(BaseAPIItemView):

    @classmethod
    def get_item_serializer(cls) -> Serializer:
        return UserSerializer()

    @classmethod
    def get_update_allowed_attributes_set(cls) -> Set[str]:
        return set()

    @classmethod
    def is_allowed_put_update(cls) -> bool:
        return False

    @classmethod
    def get_obj(cls, request: Request, user: User) -> Model:
        return user

    @classmethod
    def check_permitted_get_request_before_obj(cls, request: Request, user: User) -> None:
        LoginAPIChecker().raise_exception_if_not_valid(user)

    @classmethod
    def check_permitted_put_request_before_obj(cls, request: Request, user: User) -> None:
        raise MethodNotAllowed("PUT")

    @classmethod
    def check_permitted_delete_request_before_obj(cls, request: Request, user: User) -> None:
        raise MethodNotAllowed("DELETE")
