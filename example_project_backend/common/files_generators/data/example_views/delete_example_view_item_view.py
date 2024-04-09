from typing import Type

from django.db.models import Model
from example_app.models import ExampleModel

from common.simple_rest.async_api_request import AsyncAPIRequest
from common.simple_rest.async_views.async_delete_item_by_id_api_view import AsyncDeleteItemByIdAPIView
from common.simple_rest.permissions_checkers.login_permission_checker import LoginPermissionChecker


class DeleteExampleViewItemView(AsyncDeleteItemByIdAPIView):
    @classmethod
    def get_model_cls(cls) -> Type[Model]:
        return ExampleModel

    @classmethod
    async def check_permitted_before_object(cls, request: AsyncAPIRequest, **kwargs) -> None:
        await LoginPermissionChecker().async_raise_exception_if_not_valid(await request.future_user)

    @classmethod
    async def check_permitted_after_object(cls, request: AsyncAPIRequest, obj: ExampleModel, **kwargs) -> None:
        pass
