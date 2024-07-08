from typing import Type, Set

from django.db.models import Model
from blocks.models import Circle
from blocks.serializers.circles_serializers.full_circle_for_client_serializer import FullCircleForClientSerializer

from common.simple_rest.async_api_request import AsyncAPIRequest
from common.simple_rest.async_views.async_patch_item_by_id_api_view import AsyncPatchItemByIdAPIView
from common.simple_rest.permissions_checkers.login_permission_checker import LoginPermissionChecker
from common.simple_rest.serializers.serializer import Serializer


class PatchCircleForClientItemView(AsyncPatchItemByIdAPIView):
    @classmethod
    async def get_default_serializer(cls, **kwargs) -> Serializer:
        return FullCircleForClientSerializer()

    @classmethod
    def get_allowed_edit_fields(cls) -> Set[str]:
        return set()

    @classmethod
    def get_model_cls(cls) -> Type[Model]:
        return Circle

    @classmethod
    async def check_permitted_before_object(cls, request: AsyncAPIRequest, **kwargs) -> None:
        await LoginPermissionChecker().async_raise_exception_if_not_valid(await request.future_user)

    @classmethod
    async def check_permitted_after_object(cls, request: AsyncAPIRequest, obj: Circle, **kwargs) -> None:
        pass
