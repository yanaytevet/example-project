from typing import Type, Set

from django.db.models import Model
from example_app.models import ExampleModel
from example_app.serializers.example_models_serializers.full_example_view_serializer import FullExampleViewSerializer
from ninja import Schema, Path

from common.simple_api.api_request import APIRequest
from common.simple_api.permissions_checkers.login_permission_checker import LoginPermissionChecker
from common.simple_api.serializers.serializer import Serializer
from common.simple_api.views.create_item_api_view import CreateItemAPIView


class CreateExampleViewItemSchema(Schema):
    pass


class CreateExampleViewItemView(CreateItemAPIView):
    @classmethod
    async def check_permitted_before_creation(cls, request: APIRequest, data: Schema, path: Path) -> None:
        await LoginPermissionChecker().async_raise_exception_if_not_valid(await request.future_user)

    @classmethod
    def get_data_schema(cls) -> Type[Schema]:
        return CreateExampleViewItemSchema

    @classmethod
    def get_serializer(cls) -> Serializer:
        return FullExampleViewSerializer()

    @classmethod
    def get_model_cls(cls) -> Type[Model]:
        return ExampleModel

