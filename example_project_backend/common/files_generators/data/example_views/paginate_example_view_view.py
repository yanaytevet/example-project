from typing import Type

from django.db.models import Model, QuerySet
from example_app.models import ExampleModel
from example_app.serializers.example_models_serializers.short_example_view_serializer import ShortExampleViewSerializer
from ninja import Path, Schema, FilterSchema

from common.simple_api.api_request import APIRequest
from common.simple_api.permissions_checkers.login_permission_checker import LoginPermissionChecker
from common.simple_api.serializers.serializer import Serializer
from common.simple_api.views.pagination.paginate_items_api_view import PaginateItemsAPIView
from common.simple_api.views.pagination.pagination_input_schemas import PaginationQueryParams


class PaginationExampleViewFilterSchema(FilterSchema):
    pass


class PaginateExampleViewView(PaginateItemsAPIView):
    @classmethod
    async def check_permitted_before_pagination(cls, request: APIRequest, query: PaginationQueryParams,
                                                path: Path) -> None:
        await LoginPermissionChecker().async_raise_exception_if_not_valid(await request.future_user)

    @classmethod
    def get_serializer(cls) -> Serializer:
        return ShortExampleViewSerializer()

    @classmethod
    def get_model_cls(cls) -> Type[Model]:
        return ExampleModel

    @classmethod
    def get_filter_schema(cls) -> Type[FilterSchema]:
        return PaginationExampleViewFilterSchema

    @classmethod
    def get_allowed_order_by(cls) -> set[str]:
        return set()

