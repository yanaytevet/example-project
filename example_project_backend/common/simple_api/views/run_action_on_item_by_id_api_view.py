from abc import ABC

from ninja import Router

from common.simple_api.views.item_by_id_api_mixin import ItemByIdAPIMixin
from common.simple_api.views.run_action_on_item_api_view import RunActionOnItemAPIView


class RunActionOnItemByIdAPIView(ItemByIdAPIMixin, RunActionOnItemAPIView, ABC):
    @classmethod
    def register_post_by_id(cls, router: Router, url_suffix: str = '') -> None:
        url = '{int:object_id}/'
        if url_suffix:
            url += url_suffix
        cls.register_post(router, url)
