from typing import Type

from django.db.models import Model

from common.simple_rest.async_api_request import AsyncAPIRequest
from common.simple_rest.async_views.async_get_item_by_id_api_view import AsyncGetItemByIdAPIView
from common.simple_rest.permissions_checkers.login_permission_checker import LoginPermissionChecker
from common.simple_rest.serializers.serializer import Serializer
from example_app.models import ExampleModel
from example_app.serializers.example_models_serializers.full_example_model_serializer import FullExampleModelSerializer


class GetExampleModelItemView(AsyncGetItemByIdAPIView):
    @classmethod
    async def get_default_serializer(cls, request: AsyncAPIRequest, obj: ExampleModel, **kwargs) -> Serializer:
        return FullExampleModelSerializer()

    @classmethod
    def get_model_cls(cls) -> Type[Model]:
        return ExampleModel

    @classmethod
    async def check_permitted_before_object(cls, request: AsyncAPIRequest, **kwargs) -> None:
        await LoginPermissionChecker().async_raise_exception_if_not_valid(await request.future_user)

    @classmethod
    async def check_permitted_after_object(cls, request: AsyncAPIRequest, obj: ExampleModel, **kwargs) -> None:
        pass
