from typing import Type

from django.db.models import Model

from blocks.models import Block
from blocks.serializers.blocks_serializers.block_serializer import BlockSerializer
from common.simple_rest.async_api_request import AsyncAPIRequest
from common.simple_rest.async_views.async_post_action_item_by_id_api_view import AsyncPostActionItemByIdAPIView
from common.simple_rest.permissions_checkers.login_permission_checker import LoginPermissionChecker
from common.simple_rest.serializers.serializer import Serializer


class PostActionBuildBlockItemView(AsyncPostActionItemByIdAPIView):
    @classmethod
    async def check_permitted_before_object(cls, request: AsyncAPIRequest, **kwargs) -> None:
        await LoginPermissionChecker().async_raise_exception_if_not_valid(await request.future_user)

    @classmethod
    async def check_permitted_after_object(cls, request: AsyncAPIRequest, obj: Block, **kwargs) -> None:
        pass

    @classmethod
    def get_model_cls(cls) -> Type[Model]:
        return Block

    @classmethod
    async def get_default_serializer(cls, **kwargs) -> Serializer:
        return BlockSerializer()

    @classmethod
    async def run_action(cls, request: AsyncAPIRequest, obj: Block, **kwargs) -> None:
        should_build = request.data.get('should_build', False)
        if should_build:
            obj.a += ' build'
        else:
            obj.a += ' not build'
        await obj.asave()
