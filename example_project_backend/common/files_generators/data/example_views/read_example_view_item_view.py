from typing import Type

from django.db.models import Model

from example_app.models import ExampleModel
from example_app.serializers.example_models_serializers.full_example_view_serializer import FullExampleViewSerializer
from ninja import Path, Query

from common.simple_api.api_request import APIRequest
from common.simple_api.permissions_checkers.login_permission_checker import LoginPermissionChecker
from common.simple_api.serializers.serializer import Serializer
from common.simple_api.views.read_item_by_id_api_view import ReadItemByIdAPIView


class ReadExampleViewItemView(ReadItemByIdAPIView):
    @classmethod
    def get_serializer(cls) -> Serializer:
        return FullExampleViewSerializer()

    @classmethod
    def get_model_cls(cls) -> Type[Model]:
        return ExampleModel

    @classmethod
    async def check_permitted_before_object(cls, request: APIRequest, query: Query, path: Path) -> None:
        await LoginPermissionChecker().async_raise_exception_if_not_valid(await request.future_user)

    @classmethod
    async def check_permitted_after_object(cls, request: APIRequest, obj: ExampleModel, query: Query, path: Path) -> None:
        pass
