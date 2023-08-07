from typing import Set, Type

from django.db.models import Model
from rest_framework.request import Request

from common.consts.viewer_types import ViewerTypes
from common.django_utils.api_checkers.admin_api_checker import AdminAPIChecker
from common.django_utils.rest_utils import BaseAPIItemByIdView
from common.django_utils.serializers.serializer import Serializer
from users.models import User, ABTest
from users.serializers.a_b_test_full_serializer import ABTestFullSerializer


class ABTestFullItemByAdminView(BaseAPIItemByIdView):

    @classmethod
    def get_model_cls(cls) -> Type[Model]:
        return ABTest

    @classmethod
    def get_item_serializer(cls) -> Serializer:
        return ABTestFullSerializer()

    @classmethod
    def get_viewer_type(cls, user: User) -> ViewerTypes:
        return ViewerTypes.ADMIN

    @classmethod
    def get_update_allowed_attributes_set(cls) -> Set[str]:
        return set()

    @classmethod
    def is_allowed_put_update(cls) -> bool:
        return False

    @classmethod
    def check_permitted_any_request_before_obj(cls, request: Request, user: User) -> None:
        AdminAPIChecker().raise_exception_if_not_valid(user)
