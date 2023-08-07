from typing import Set

from django.db.models import Model
from rest_framework.request import Request

from common.consts.viewer_types import ViewerTypes
from common.django_utils.api_checkers.org_manager_api_checker import OrgManagerAPIChecker
from common.django_utils.rest_utils import BaseAPIItemView
from common.django_utils.serializers.serializer import Serializer
from users.models import User
from users.serializers.organization_serializer import OrganizationSerializer


class MyOrganizationByManagerView(BaseAPIItemView):

    @classmethod
    def get_item_serializer(cls) -> Serializer:
        return OrganizationSerializer()

    @classmethod
    def get_viewer_type(cls, user: User) -> ViewerTypes:
        return ViewerTypes.CLIENT

    @classmethod
    def get_obj(cls, request: Request, user: User) -> Model:
        return user.organization

    @classmethod
    def get_update_allowed_attributes_set(cls) -> Set[str]:
        return {"description"}

    @classmethod
    def is_allowed_put_update(cls) -> bool:
        return True

    @classmethod
    def check_permitted_any_request_before_obj(cls, request: Request, user: User) -> None:
        OrgManagerAPIChecker().raise_exception_if_not_valid(user)


