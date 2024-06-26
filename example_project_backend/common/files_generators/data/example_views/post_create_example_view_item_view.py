from typing import Type, Set

from django.db.models import Model
from example_app.models import ExampleModel
from example_app.serializers.example_models_serializers.full_example_view_serializer import FullExampleViewSerializer

from common.simple_rest.async_api_request import AsyncAPIRequest
from common.simple_rest.async_views.async_post_create_api_view import AsyncPostCreateAPIView
from common.simple_rest.permissions_checkers.login_permission_checker import LoginPermissionChecker
from common.simple_rest.serializers.serializer import Serializer


class PostCreateExampleViewItemView(AsyncPostCreateAPIView):
    @classmethod
    async def check_permitted(cls, request: AsyncAPIRequest, **kwargs) -> None:
        await LoginPermissionChecker().async_raise_exception_if_not_valid(await request.future_user)

    @classmethod
    def get_allowed_creation_fields(cls) -> Set[str]:
        return set()

    @classmethod
    def get_model_cls(cls) -> Type[Model]:
        return ExampleModel

    @classmethod
    async def get_default_serializer(cls, request: AsyncAPIRequest, obj: Model, **kwargs) -> Serializer:
        return FullExampleViewSerializer()
