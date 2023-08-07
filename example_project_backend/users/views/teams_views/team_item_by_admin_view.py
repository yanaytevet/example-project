from typing import Set, Type

from django.db.models import Model
from rest_framework.request import Request

from common.consts.viewer_types import ViewerTypes
from common.django_utils.api_checkers.admin_api_checker import AdminAPIChecker
from common.django_utils.rest_utils import BaseAPIItemByIdView
from common.django_utils.serializers.serializer import Serializer
from users.models import User, Team
from users.serializers.team_serializer import TeamSerializer


class TeamItemByAdminView(BaseAPIItemByIdView):

    @classmethod
    def get_model_cls(cls) -> Type[Model]:
        return Team

    @classmethod
    def get_item_serializer(cls) -> Serializer:
        return TeamSerializer()

    @classmethod
    def get_viewer_type(cls, user: User) -> ViewerTypes:
        return ViewerTypes.ADMIN

    @classmethod
    def get_update_allowed_attributes_set(cls) -> Set[str]:
        return {"name"}

    @classmethod
    def is_allowed_put_update(cls) -> bool:
        return True

    @classmethod
    def check_permitted_any_request_before_obj(cls, request: Request, user: User) -> None:
        AdminAPIChecker().raise_exception_if_not_valid(user)
