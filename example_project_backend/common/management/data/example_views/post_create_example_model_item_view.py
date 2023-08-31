from typing import Type, Set

from django.db.models import Model
from example_app.models import ExampleModel
from example_app.serializers.example_models_serializers.full_example_model_serializer import FullExampleModelSerializer

from common.simple_rest.async_api_request import AsyncAPIRequest
from common.simple_rest.async_views.async_post_create_api_view import AsyncPostCreateAPIView
from common.simple_rest.permissions_checkers.login_permission_checker import LoginPermissionChecker
from common.type_hints import JSONType


class PostCreateExampleModelItemView(AsyncPostCreateAPIView):
    @classmethod
    async def check_permitted(cls, request: AsyncAPIRequest, **kwargs) -> None:
        await LoginPermissionChecker().async_raise_exception_if_not_valid(await request.future_user)

    @classmethod
    def get_allowed_creation_fields(cls) -> Set[str]:
        return set()

    @classmethod
    async def serialize_object(cls, request: AsyncAPIRequest, obj: ExampleModel, **kwargs) -> JSONType:
        return await FullExampleModelSerializer().async_serialize(obj)

    @classmethod
    def get_model_cls(cls) -> Type[Model]:
        return ExampleModel
