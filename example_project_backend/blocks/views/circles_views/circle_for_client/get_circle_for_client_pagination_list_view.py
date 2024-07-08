from typing import Type

from django.db.models import Model, QuerySet
from blocks.models import Circle
from blocks.serializers.circles_serializers.short_circle_for_client_serializer import ShortCircleForClientSerializer

from common.simple_rest.async_api_request import AsyncAPIRequest
from common.simple_rest.async_views.async_get_list_api_view import AsyncGetListAPIView
from common.simple_rest.permissions_checkers.login_permission_checker import LoginPermissionChecker
from common.simple_rest.query_filters.base_query_filter import BaseQueryFilter
from common.simple_rest.serializers.serializer import Serializer


class GetCircleForClientPaginationListView(AsyncGetListAPIView):
    @classmethod
    async def get_mandatory_query_filters(cls, request: AsyncAPIRequest, objects: QuerySet, **kwargs
                                          ) -> list[BaseQueryFilter]:
        return []

    @classmethod
    async def get_optional_query_filter_classes_by_name(cls, request: AsyncAPIRequest, **kwargs
                                                        ) -> dict[str, Type[BaseQueryFilter]]:
        return {}

    @classmethod
    async def get_default_serializer(cls, **kwargs) -> Serializer:
        return ShortCircleForClientSerializer()

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
    def get_model_cls(cls) -> Type[Model]:
        return Circle
