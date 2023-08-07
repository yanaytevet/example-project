from typing import Set, Type

from django.db.models import Model
from rest_framework.request import Request

from common.consts.viewer_types import ViewerTypes
from common.django_utils.api_checkers.org_manager_api_checker import OrgManagerAPIChecker
from common.django_utils.rest_utils import BaseAPIItemByIdView
from common.django_utils.serializers.serializer import Serializer
from users.models import User, Team
from users.apis_checkers.teams_api_checkers import TeamBelongToOrgAPIChecker
from users.serializers.team_serializer import TeamSerializer


class TeamItemByManagerView(BaseAPIItemByIdView):

    @classmethod
    def get_model_cls(cls) -> Type[Model]:
        return Team

    @classmethod
    def get_item_serializer(cls) -> Serializer:
        return TeamSerializer()

    @classmethod
    def get_viewer_type(cls, user: User) -> ViewerTypes:
        return ViewerTypes.CLIENT

    @classmethod
    def get_update_allowed_attributes_set(cls) -> Set[str]:
        return {"name"}

    @classmethod
    def is_allowed_put_update(cls) -> bool:
        return True

    @classmethod
    def check_permitted_any_request_before_obj(cls, request: Request, user: User) -> None:
        OrgManagerAPIChecker().raise_exception_if_not_valid(user)

    @classmethod
    def check_permitted_any_request_after_obj(cls, request: Request, user: User, obj: Team) -> None:
        TeamBelongToOrgAPIChecker().raise_exception_if_not_valid(obj, user.organization)
