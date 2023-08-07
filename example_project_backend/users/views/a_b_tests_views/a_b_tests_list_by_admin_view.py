from typing import Set, Type

from django.db.models import Model, QuerySet
from rest_framework.request import Request

from common.consts.viewer_types import ViewerTypes
from common.django_utils.api_checkers.admin_api_checker import AdminAPIChecker
from common.django_utils.api_checkers.request_data_fields_api_checker import RequestDataFieldsAPIChecker
from common.django_utils.rest_utils import BaseAPIListView
from common.django_utils.serializers.serializer import Serializer
from users.models import User, ABTest
from users.serializers.a_b_test_serializer import ABTestSerializer


class ABTestsListByAdminView(BaseAPIListView):

    @classmethod
    def get_model_cls(cls) -> Type[Model]:
        return ABTest

    @classmethod
    def get_item_serializer(cls) -> Serializer:
        return ABTestSerializer()

    @classmethod
    def get_list_serializer(cls) -> Serializer:
        return ABTestSerializer()

    @classmethod
    def get_viewer_type(cls, user: User) -> ViewerTypes:
        return ViewerTypes.ADMIN

    @classmethod
    def modify_objects_for_request(cls, request: Request, user: User, objects: QuerySet) -> QuerySet:
        return objects.order_by('-end_time', '-start_time')

    @classmethod
    def get_create_allowed_attributes_set(cls) -> Set[str]:
        return {"name", "description"}

    @classmethod
    def check_permitted_any_request(cls, request: Request, user: User) -> None:
        AdminAPIChecker().raise_exception_if_not_valid(user)

    @classmethod
    def check_permitted_post_request(cls, request: Request, user: User) -> None:
        RequestDataFieldsAPIChecker(["name"]).raise_exception_if_not_valid(request)
