from typing import Set, Type

from django.db.models import Model, QuerySet, Q
from rest_framework.exceptions import MethodNotAllowed
from rest_framework.request import Request

from common.consts.viewer_types import ViewerTypes
from common.django_utils.api_checkers.admin_api_checker import AdminAPIChecker
from common.django_utils.rest_utils import BaseAPIListView
from common.django_utils.serializers.serializer import Serializer
from users.models import User, UserEvent
from users.serializers.user_event_serializer import UserEventSerializer


class UserEventsListByAdminView(BaseAPIListView):
    @classmethod
    def get_model_cls(cls) -> Type[Model]:
        return UserEvent

    @classmethod
    def get_item_serializer(cls) -> Serializer:
        return UserEventSerializer()

    @classmethod
    def get_list_serializer(cls) -> Serializer:
        return UserEventSerializer()

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
        text = request.query_params.get('text', '')
        objects = objects.filter(
            Q(user__person_info__first_name__contains=text)
            | Q(user__person_info__last_name__contains=text)
            | Q(user__person_info__emails__icontains=text)
            | Q(name__contains=text)
            | Q(attributes__icontains=text)
        )
        return objects.order_by('-creation_time')[:100]

    @classmethod
    def check_permitted_post_request(cls, request: Request, user: User) -> None:
        MethodNotAllowed('POST')
