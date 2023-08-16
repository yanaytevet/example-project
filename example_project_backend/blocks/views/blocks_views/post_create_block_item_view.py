from typing import Type, Set

from django.db.models import Model

from blocks.models import Block
from blocks.serializers.block_serializer import BlockSerializer
from common.simple_rest.async_api_request import AsyncAPIRequest
from common.simple_rest.async_views.async_post_create_api_view import AsyncPostCreateAPIView
from common.simple_rest.permissions_checkers.login_permission_checker import LoginPermissionChecker
from common.type_hints import JSONType


class PostCreateBlockItemView(AsyncPostCreateAPIView):
    @classmethod
    async def check_permitted(cls, request: AsyncAPIRequest, **kwargs) -> None:
        await LoginPermissionChecker().async_raise_exception_if_not_valid(await request.future_user)

    @classmethod
    def get_allowed_creation_fields(cls) -> Set[str]:
        return {'a', 'b', 'c', 'block_type'}

    @classmethod
    async def serialize_object(cls, request: AsyncAPIRequest, obj: Block, **kwargs) -> JSONType:
        return await BlockSerializer().async_serialize(obj)

    @classmethod
    def get_model_cls(cls) -> Type[Model]:
        return Block
