from abc import ABC

from .async_item_by_id_api_mixin import AsyncItemByIdAPIMixin
from .async_post_action_item_api_view import AsyncPostActionItemAPIView


class AsyncPostActionItemByIdAPIView(AsyncItemByIdAPIMixin, AsyncPostActionItemAPIView, ABC):
    pass
