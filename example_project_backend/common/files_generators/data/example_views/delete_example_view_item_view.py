from typing import Type

from django.db.models import Model
from example_app.models import ExampleModel
from ninja import Path, Schema

from common.simple_api.api_request import APIRequest
from common.simple_api.permissions_checkers.login_permission_checker import LoginPermissionChecker
from common.simple_api.views.delete_item_by_id_api_view import DeleteItemByIdAPIView


class DeleteExampleViewItemView(DeleteItemByIdAPIView):
    @classmethod
    def get_model_cls(cls) -> Type[Model]:
        return ExampleModel

    @classmethod
    async def check_permitted_before_object(cls, request: APIRequest, data: Schema, path: Path) -> None:
        await LoginPermissionChecker().async_raise_exception_if_not_valid(await request.future_user)

    @classmethod
    async def check_permitted_after_object(cls, request: APIRequest, obj: ExampleModel, data: Schema, path: Path) -> None:
        pass
