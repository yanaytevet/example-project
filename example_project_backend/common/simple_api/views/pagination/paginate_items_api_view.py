from abc import ABC, abstractmethod
from typing import Type

from django.db.models import Model, QuerySet
from django.http import HttpRequest
from ninja import Router, Schema, Path, FilterSchema, Query

from common.simple_api.api_request import APIRequest
from common.simple_api.schemas.empty_schema import EmptySchema
from common.simple_api.views.pagination.pagination_input_schemas import PaginationQueryParams
from common.simple_api.views.pagination.pagination_output import PaginationOutput
from common.simple_api.views.serialize_item_mixin import SerializeItemMixin


class PaginateItemsAPIView(SerializeItemMixin, ABC):
    @classmethod
    def register_get(cls, router: Router, url: str = '') -> None:
        resp_schema = cls.get_output_schema()
        filter_schema = cls.get_filter_schema()
        path_schema = cls.get_path_args_schema()

        @router.get(url, response=PaginationOutput[resp_schema], tags=cls.get_tags(), operation_id=cls.__name__)
        async def pagination(request: HttpRequest,
                             query: Query[PaginationQueryParams] = None,
                             filters: filter_schema = Query(default=None),
                             path: Path[path_schema] = None) -> PaginationOutput[resp_schema]:
            api_request = APIRequest(request)
            return await cls().run(api_request, query, filters, path)

    async def run(self, request: APIRequest, query: PaginationQueryParams, filters: FilterSchema, path: Path) -> PaginationOutput:
        await self.check_permitted_before_pagination(request, query, path)
        query_set = self.get_model_cls().objects.all()
        query_set = self.apply_initial_filter_and_order(query_set, query, path)
        if filters:
            query_set = filters.filter(query_set)
        query_set = self.apply_order_by(query_set, query, path)
        query_set = self.apply_final_filter(query_set, query, path)
        page = query.page
        page_size = query.page_size
        offset = page * page_size
        paginated_query_set = query_set[offset:offset + page_size]

        total = await query_set.acount()
        total_pages = (total + page_size - 1) // page_size

        output = PaginationOutput(
            total_amount=total,
            pages_amount=total_pages,
            page=page,
            page_size=page_size,
            data=await self.serialize_query_set(request, paginated_query_set),
        )
        return output

    @classmethod
    @abstractmethod
    def get_model_cls(cls) -> Type[Model]:
        raise NotImplementedError()

    @classmethod
    def apply_initial_filter_and_order(cls, query_set: QuerySet, query: PaginationQueryParams, path: Path) -> QuerySet:
        return query_set.order_by('id')

    @classmethod
    def apply_order_by(cls, query_set: QuerySet, query: PaginationQueryParams, path: Path) -> QuerySet:
        if not query.order_by:
            return query_set
        allowed_order_by_set = cls.get_allowed_order_by()
        for order_by_item in query.order_by:
            clear_order_by_item = order_by_item.lstrip('-')
            if clear_order_by_item not in allowed_order_by_set:
                raise ValueError(f'order_by item {order_by_item} is not allowed')
        return query_set.order_by(*query.order_by)

    @classmethod
    def apply_final_filter(cls, query_set: QuerySet, query: PaginationQueryParams, path: Path) -> QuerySet:
        return query_set

    @classmethod
    @abstractmethod
    async def check_permitted_before_pagination(cls, request: APIRequest, query: PaginationQueryParams, path: Path
                                                ) -> None:
        raise NotImplementedError()

    @classmethod
    def get_output_schema(cls) -> Type[Schema]:
        return cls.get_serializer().get_output_schema()

    @classmethod
    @abstractmethod
    def get_filter_schema(cls) -> Type[FilterSchema]:
        raise NotImplementedError()

    @classmethod
    @abstractmethod
    def get_allowed_order_by(cls) -> set[str]:
        raise NotImplementedError()

    @classmethod
    def get_path_args_schema(cls) -> Type[Schema]:
        return EmptySchema

    @classmethod
    def get_tags(cls) -> list[str]:
        return [cls.get_model_cls().__name__]
