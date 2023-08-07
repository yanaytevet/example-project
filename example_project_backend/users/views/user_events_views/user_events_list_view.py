from typing import Set, Type

from django.db.models import Model
from rest_framework.request import Request

from common.consts.viewer_types import ViewerTypes
from common.django_utils.api_checkers.admin_api_checker import AdminAPIChecker
from common.django_utils.api_checkers.login_api_checker import LoginAPIChecker
from common.django_utils.rest_utils import BaseAPIListView
from common.django_utils.serializers.empty_serializer import EmptySerializer
from common.django_utils.serializers.serializer import Serializer
from common.type_hints import JSONType
from users.models import User, UserEvent
from users.tasks.run_events_analysis import run_events_analysis


class UserEventsListView(BaseAPIListView):

    @classmethod
    def get_model_cls(cls) -> Type[Model]:
        return UserEvent

    @classmethod
    def get_item_serializer(cls) -> Serializer:
        return EmptySerializer()

    @classmethod
    def get_list_serializer(cls) -> Serializer:
        return EmptySerializer()

    @classmethod
    def get_viewer_type(cls, user: User) -> ViewerTypes:
        return ViewerTypes.CLIENT

    @classmethod
    def get_create_allowed_attributes_set(cls) -> Set[str]:
        return {'name', 'tab_id', 'attributes', 'user_id'}

    @classmethod
    def check_permitted_get_request(cls, request: Request, user: User) -> None:
        AdminAPIChecker().raise_exception_if_not_valid(user)

    @classmethod
    def check_permitted_post_request(cls, request: Request, user: User) -> None:
        pass

    @classmethod
    def get_modified_request_data_for_post(cls, request: Request, user: User) -> JSONType:
        if request.session.get('as_other', False):
            return {}
        data = dict(request.data)
        data["user_id"] = user.id if LoginAPIChecker().is_valid(user) else None
        return data

    @classmethod
    def run_after_post(cls, request: Request, user: User, obj: UserEvent) -> None:
        if obj and obj.id:
            run_events_analysis.delay(obj.id)
