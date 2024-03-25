from typing import Type

from django.db.models import Model

from blocks.models import Block
from blocks.serializers.blocks_serializers.block_serializer import BlockSerializer
from common.simple_rest.async_api_request import AsyncAPIRequest
from common.simple_rest.async_views.async_get_item_by_id_api_view import AsyncGetItemByIdAPIView
from common.simple_rest.permissions_checkers.login_permission_checker import LoginPermissionChecker
from common.simple_rest.serializers.serializer import Serializer
from common.type_hints import JSONType


class GetBlockItemView(AsyncGetItemByIdAPIView):
    @classmethod
    async def get_default_serializer(cls, request: AsyncAPIRequest, obj: Block, **kwargs) -> Serializer:
        return await BlockSerializer().async_serialize(obj)

    @classmethod
    def get_model_cls(cls) -> Type[Model]:
        return Block

    @classmethod
    async def check_permitted_before_object(cls, request: AsyncAPIRequest, **kwargs) -> None:
        await LoginPermissionChecker().async_raise_exception_if_not_valid(await request.future_user)

    @classmethod
    async def check_permitted_after_object(cls, request: AsyncAPIRequest, obj: Model, **kwargs) -> None:
        pass
