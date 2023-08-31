from typing import Type

from django.db.models import Model
from example_app.models import ExampleModel
from example_app.serializers.example_models_serializers.short_example_model_serializer import \
    ShortExampleModelSerializer

from common.simple_rest.async_api_request import AsyncAPIRequest
from common.simple_rest.async_views.async_get_list_api_view import AsyncGetListAPIView
from common.simple_rest.permissions_checkers.login_permission_checker import LoginPermissionChecker
from common.type_hints import JSONType


class GetPaginationExampleModelListView(AsyncGetListAPIView):
    @classmethod
    def get_allowed_filters(cls) -> set[str]:
        return set()

    @classmethod
    def get_allowed_order_by(cls) -> set[str]:
        return set()

    @classmethod
    async def check_permitted(cls, request: AsyncAPIRequest, **kwargs) -> None:
        await LoginPermissionChecker().async_raise_exception_if_not_valid(await request.future_user)

    @classmethod
    async def serialize_object(cls, request: AsyncAPIRequest, obj: ExampleModel, **kwargs) -> JSONType:
        return await ShortExampleModelSerializer().async_serialize(obj)

    @classmethod
    def get_model_cls(cls) -> Type[Model]:
        return ExampleModel
