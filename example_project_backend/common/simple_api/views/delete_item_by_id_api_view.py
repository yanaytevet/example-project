from abc import ABC

from ninja import Router

from common.simple_api.views.delete_item_api_view import DeleteItemAPIView
from common.simple_api.views.item_by_id_api_mixin import ItemByIdAPIMixin


class DeleteItemByIdAPIView(ItemByIdAPIMixin, DeleteItemAPIView, ABC):
    @classmethod
    def register_delete_by_id(cls, router: Router) -> None:
        cls.register_delete(router, '{int:object_id}/')
