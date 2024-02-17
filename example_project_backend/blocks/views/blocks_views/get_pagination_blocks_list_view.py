from typing import Type

from django.db.models import Model

from blocks.models import Block
from blocks.serializers.blocks_serializers.block_serializer import BlockSerializer
from common.simple_rest.async_api_request import AsyncAPIRequest
from common.simple_rest.async_views.async_get_list_api_view import AsyncGetListAPIView
from common.simple_rest.permissions_checkers.login_permission_checker import LoginPermissionChecker
from common.type_hints import JSONType


class GetPaginationBlockListView(AsyncGetListAPIView):
    @classmethod
    def get_allowed_filters(cls) -> set[str]:
        return {'a', 'c', 'block_type'}

    @classmethod
    def get_allowed_order_by(cls) -> set[str]:
        return {'a', 'b', 'c'}

    @classmethod
    async def check_permitted(cls, request: AsyncAPIRequest, **kwargs) -> None:
        await LoginPermissionChecker().async_raise_exception_if_not_valid(await request.future_user)

    @classmethod
    async def serialize_object(cls, request: AsyncAPIRequest, obj: Block, **kwargs) -> JSONType:
        return await BlockSerializer().async_serialize(obj)

    @classmethod
    def get_model_cls(cls) -> Type[Model]:
        return Block
