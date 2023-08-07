from typing import Set, Type

from django.db.models import Model
from rest_framework.request import Request

from common.consts.viewer_types import ViewerTypes
from common.django_utils.api_checkers.admin_api_checker import AdminAPIChecker
from common.django_utils.api_checkers.request_data_fields_api_checker import RequestDataFieldsAPIChecker
from common.django_utils.rest_utils import BaseAPIListView
from common.django_utils.serializers.serializer import Serializer
from users.models import User, Team
from users.serializers.short_team_serializer import ShortTeamSerializer
from users.serializers.team_serializer import TeamSerializer


class TeamsListByAdminView(BaseAPIListView):

    @classmethod
    def get_model_cls(cls) -> Type[Model]:
        return Team

    @classmethod
    def get_item_serializer(cls) -> Serializer:
        return TeamSerializer()

    @classmethod
    def get_list_serializer(cls) -> Serializer:
        return ShortTeamSerializer()

    @classmethod
    def get_viewer_type(cls, user: User) -> ViewerTypes:
        return ViewerTypes.ADMIN

    @classmethod
    def get_create_allowed_attributes_set(cls) -> Set[str]:
        return {"name", "organization_id"}

    @classmethod
    def check_permitted_any_request(cls, request: Request, user: User) -> None:
        AdminAPIChecker().raise_exception_if_not_valid(user)

    @classmethod
    def check_permitted_post_request(cls, request: Request, user: User) -> None:
        RequestDataFieldsAPIChecker(["name", "organization_id"]).raise_exception_if_not_valid(request)
