import json
import math
from abc import ABC, abstractmethod
from typing import Type, Iterable

from django.db.models import Model, QuerySet, Q
from django.http import HttpRequest, JsonResponse, HttpResponse

from common.type_hints import JSONType
from .async_api_view_component import AsyncAPIViewComponent
from .serialize_item_mixin import SerializeItemMixin
from ..api_request import APIRequest
from ..async_api_request import AsyncAPIRequest
from ..enums.methods import Methods
from ..enums.queries_logic_operators import QueriesLogicOperators
from ..enums.status_code import StatusCode
from ..query_filters.base_query_filter import BaseQueryFilter


def create_has_one_of_filter(real_key: str, values: list[str]):
    q_objects = [Q(**{f'{real_key}__contains': value}) for value in values]
    final_q_object = q_objects[0]
    for q_object in q_objects[1:]:
        final_q_object |= q_object
    return final_q_object


def create_ihas_one_of_filter(real_key: str, values: list[str]):
    q_objects = [Q(**{f'{real_key}__icontains': f'"{value}"'}) for value in values]
    final_q_object = q_objects[0]
    for q_object in q_objects[1:]:
        final_q_object |= q_object
    return final_q_object


class AsyncGetListAPIView(SerializeItemMixin, AsyncAPIViewComponent, ABC):
    DEFAULT_PAGE_SIZE = 25
    MIN_PAGE_SIZE = 10
    MAX_PAGE_SIZE = 100

    QUERY_STR_TO_FUNC = {
        'has_one_of': create_has_one_of_filter,
        'ihas_one_of': create_ihas_one_of_filter,
    }

    @classmethod
    def get_method(cls) -> Methods:
        return Methods.GET

    async def get(self, request: HttpRequest, **kwargs) -> HttpResponse:
        return await self.run_with_exception_handling(AsyncAPIRequest(request), **kwargs)

    async def run(self, request: AsyncAPIRequest, **kwargs) -> JsonResponse:
        await self.check_permitted(request, **kwargs)
        objects = await self.get_query_set(request, **kwargs)
        objects = await self.filter_objects_by_request(request, objects, **kwargs)
        objects = await self.order_objects_by_request(request, objects, **kwargs)
        page = int(request.query_params.get('page', 0))
        page_size = self.get_page_size(request)

        total_amount = await objects.acount()
        page = self.get_correct_page(total_amount, page, page_size)
        data = await self.serialize_objects(request, objects, page, page_size, **kwargs)
        res = {
            'total_amount': total_amount,
            'pages_amount': math.ceil(total_amount / page_size),
            'data': data,
            'page': page,
            'page_size': page_size,
        }
        return JsonResponse(res, status=StatusCode.HTTP_200_OK, safe=False)

    @classmethod
    @abstractmethod
    async def check_permitted(cls, request: AsyncAPIRequest, **kwargs) -> None:
        raise NotImplementedError()

    @classmethod
    async def get_query_set(cls, request: AsyncAPIRequest, **kwargs) -> QuerySet:
        """
        use case: if you want to annotate the query set with some data, override this method
        """
        return cls.get_model_cls().objects

    @classmethod
    @abstractmethod
    def get_model_cls(cls) -> Type[Model]:
        raise NotImplementedError()

    @classmethod
    async def filter_objects_by_request(cls, request: AsyncAPIRequest, objects: QuerySet, **kwargs) -> QuerySet:
        objects = await cls.filter_objects_by_mandatory_filters(request, objects, **kwargs)
        objects = await cls.filter_objects_by_queries_params(request, objects, **kwargs)
        objects = await cls.filter_objects_by_optional_filters(request, objects, **kwargs)
        return objects

    @classmethod
    async def filter_objects_by_mandatory_filters(cls, request: AsyncAPIRequest, objects: QuerySet, **kwargs) \
            -> QuerySet:
        for query_filter in await cls.get_mandatory_query_filters(request, objects, **kwargs):
            objects = await query_filter.run(objects)
        return objects

    @classmethod
    @abstractmethod
    async def get_mandatory_query_filters(cls, request: AsyncAPIRequest, objects: QuerySet, **kwargs) \
            -> list[BaseQueryFilter]:
        raise NotImplementedError()

    @classmethod
    async def filter_objects_by_queries_params(cls, request: AsyncAPIRequest, objects: QuerySet, **kwargs) -> QuerySet:
        filters_dict = {}
        special_filters = []
        allowed_filters = cls.get_allowed_filters()

        for key, value in cls.get_params_from_request(request, 'filter', {}).items():
            if cls.does_key_exist_in_allowed_filters(key, allowed_filters):
                if cls.has_none_values_in(key, value):
                    special_filters.append(Q(**{f'{key[:-4]}__isnull': True}) | Q(**{key: value}))
                key_split_arr = key.split('__')
                if key_split_arr[-1] in cls.QUERY_STR_TO_FUNC:
                    real_key = '__'.join(key_split_arr[:-1])
                    special_filters.append(cls.QUERY_STR_TO_FUNC[key_split_arr[-1]](real_key, value))
                else:
                    filters_dict[key] = value

        return objects.filter(**filters_dict).filter(*special_filters)

    @classmethod
    @abstractmethod
    def get_allowed_filters(cls) -> set[str]:
        raise NotImplementedError()

    @classmethod
    def does_key_exist_in_allowed_filters(cls, key: str, allowed_filters: set[str]) -> bool:
        if '__' in key:
            key = '__'.join(key.split('__')[:-1])
        return key in allowed_filters

    @classmethod
    def has_none_values_in(cls, key: str, value: list[str]) -> bool:
        return key.endswith('__in') and None in value

    @classmethod
    async def filter_objects_by_optional_filters(cls, request: AsyncAPIRequest, objects: QuerySet, **kwargs) -> QuerySet:
        optional_filters_operator = await cls.get_optional_queries_operator(request, **kwargs)
        res = None
        if optional_filters_operator == QueriesLogicOperators.AND:
            res = objects
        async for query_filter in cls.get_optional_query_filters(request, objects, **kwargs):
            if optional_filters_operator == QueriesLogicOperators.OR:
                if res is None:
                    res = await query_filter.run(objects)
                else:
                    res = res.union(await query_filter.run(objects))
            elif optional_filters_operator == QueriesLogicOperators.AND:
                res = await query_filter.run(res)
        if res is None:
            res = objects
        return res

    @classmethod
    async def get_optional_queries_operator(cls, request: AsyncAPIRequest, **kwargs) -> QueriesLogicOperators:
        return cls.get_params_from_request(request, 'optional_queries_operator', 'and')

    @classmethod
    async def get_optional_query_filters(cls, request: AsyncAPIRequest, objects: QuerySet, **kwargs) \
            -> Iterable[BaseQueryFilter]:
        optional_filters_and_data = cls.get_params_from_request(request, 'optional_filters', [])
        optional_query_filter_classes_by_name = await cls.get_optional_query_filter_classes_by_name(request, **kwargs)
        for filter_name, data in optional_filters_and_data:
            query_filter_cls = optional_query_filter_classes_by_name[filter_name]
            yield query_filter_cls.create_from_request_and_data(request, data, **kwargs)

    @classmethod
    @abstractmethod
    async def get_optional_query_filter_classes_by_name(cls, request: AsyncAPIRequest, **kwargs) \
            -> dict[str, BaseQueryFilter]:
        raise NotImplementedError()

    @classmethod
    async def order_objects_by_request(cls, request: AsyncAPIRequest, objects: QuerySet, **kwargs) -> QuerySet:
        order_by_list = []
        allowed_order_by = cls.get_allowed_order_by()

        for value in cls.get_params_from_request(request, 'order_by', []):
            if cls.does_key_exist_in_allowed_order_by(value, allowed_order_by):
                order_by_list.append(value)
        if not order_by_list:
            order_by_list = cls.get_order_by_default_list()
        return objects.order_by(*order_by_list)

    @classmethod
    def get_order_by_default_list(cls) -> list[str]:
        return ['id']

    @classmethod
    @abstractmethod
    def get_allowed_order_by(cls) -> set[str]:
        raise NotImplementedError()

    @classmethod
    def does_key_exist_in_allowed_order_by(cls, key: str, allowed_order_by: set[str]) -> bool:
        if key.startswith('-'):
            key = key[1:]
        return key in allowed_order_by

    @classmethod
    def get_params_from_request(cls, request: APIRequest, key: str, default_value: JSONType) -> JSONType:
        params_str = request.query_params.get(key)
        if not params_str:
            return default_value
        return json.loads(params_str)

    @classmethod
    def get_page_size(cls, request: AsyncAPIRequest) -> int:
        page_size = int(request.query_params.get('page_size', cls.DEFAULT_PAGE_SIZE))
        return min(max(cls.MIN_PAGE_SIZE, page_size), cls.MAX_PAGE_SIZE)

    @classmethod
    async def serialize_objects(cls, request: AsyncAPIRequest, objects: QuerySet, page: int, page_size: int,
                                **kwargs) -> list[JSONType]:
        start = page * page_size
        end = (page + 1) * page_size
        return [await cls.serialize_object(request, obj, **kwargs) async for obj in objects[start: end]]

    @classmethod
    def get_correct_page(cls, total_amount: int, page: int, page_size: int) -> int:
        if page < 0:
            return 0
        if page * page_size > total_amount:
            return max(0, math.ceil(total_amount / page_size) - 1)
        return page
