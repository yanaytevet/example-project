from typing import Set, Type

from django.db.models import Model
from rest_framework.request import Request

from common.consts.viewer_types import ViewerTypes
from common.django_utils.api_checkers.admin_api_checker import AdminAPIChecker
from common.django_utils.api_checkers.request_data_fields_api_checker import RequestDataFieldsAPIChecker
from common.django_utils.rest_utils import BaseAPIItemByIdView
from common.django_utils.serializers.serializer import Serializer
from common.time_utils import TimeUtils
from users.models import User, ABTest
from users.serializers.a_b_test_serializer import ABTestSerializer


class ABTestItemByAdminView(BaseAPIItemByIdView):

    @classmethod
    def get_model_cls(cls) -> Type[Model]:
        return ABTest

    @classmethod
    def get_item_serializer(cls) -> Serializer:
        return ABTestSerializer()

    @classmethod
    def get_viewer_type(cls, user: User) -> ViewerTypes:
        return ViewerTypes.ADMIN

    @classmethod
    def get_update_allowed_attributes_set(cls) -> Set[str]:
        return {"name", 'description'}

    @classmethod
    def is_allowed_put_update(cls) -> bool:
        return True

    def put_update_start_time(self, request: Request, user: User, obj: ABTest) -> None:
        RequestDataFieldsAPIChecker(['start_time']).raise_exception_if_not_valid(request=request)
        start_time_str = request.data['start_time']
        obj.start_time = TimeUtils.from_default_str(start_time_str)
        obj.save()

    def put_update_end_time(self, request: Request, user: User, obj: ABTest) -> None:
        RequestDataFieldsAPIChecker(['end_time']).raise_exception_if_not_valid(request=request)
        end_time_str = request.data['end_time']
        obj.end_time = TimeUtils.from_default_str(end_time_str)
        obj.save()

    def put_finish(self, request: Request, user: User, obj: ABTest) -> None:
        obj.end_time = TimeUtils.now()
        obj.save()

    def put_clear_end_time(self, request: Request, user: User, obj: ABTest) -> None:
        obj.end_time = None
        obj.save()

    @classmethod
    def check_permitted_any_request_before_obj(cls, request: Request, user: User) -> None:
        AdminAPIChecker().raise_exception_if_not_valid(user)
