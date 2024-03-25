from typing import Type

from django.db.models import Model

from blocks.item_actions.blocks_item_actions.build_block_put_action import BuildBlockItemAction
from blocks.models import Block
from blocks.serializers.blocks_serializers.block_serializer import BlockSerializer
from common.simple_rest.async_api_request import AsyncAPIRequest
from common.simple_rest.async_views.async_put_actions_item_by_id_api_view import AsyncPutActionsItemByIdAPIView
from common.simple_rest.permissions_checkers.login_permission_checker import LoginPermissionChecker
from common.simple_rest.item_actions.base_put_action import BaseItemAction
from common.simple_rest.serializers.serializer import Serializer


class PutActionsBlockItemView(AsyncPutActionsItemByIdAPIView):
    @classmethod
    async def get_put_action_classes_by_name(cls, request: AsyncAPIRequest, obj: Model, **kwargs) \
            -> dict[str, type[BaseItemAction]]:
        return {
            'build': BuildBlockItemAction
        }

    @classmethod
    async def get_default_serializer(cls, request: AsyncAPIRequest, obj: Model, **kwargs) -> Serializer:
        return BlockSerializer()

    @classmethod
    def get_model_cls(cls) -> Type[Model]:
        return Block

    @classmethod
    async def check_permitted_before_object(cls, request: AsyncAPIRequest, **kwargs) -> None:
        await LoginPermissionChecker().async_raise_exception_if_not_valid(await request.future_user)

    @classmethod
    async def check_permitted_after_object(cls, request: AsyncAPIRequest, obj: Block, **kwargs) -> None:
        pass
