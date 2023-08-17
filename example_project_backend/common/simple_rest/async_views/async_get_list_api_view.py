import json
import math
from abc import ABC, abstractmethod
from typing import Type

from django.db.models import Model, QuerySet
from django.http import HttpRequest, JsonResponse, HttpResponse

from .async_api_view_component import AsyncAPIViewComponent
from ..api_request import APIRequest
from ..async_api_request import AsyncAPIRequest
from common.type_hints import JSONType
from ..constants.methods import Methods
from ..constants.status_code import StatusCode


class AsyncGetListAPIView(AsyncAPIViewComponent, ABC):
    DEFAULT_PAGE_SIZE = 25
    MIN_PAGE_SIZE = 10
    MAX_PAGE_SIZE = 100

    @classmethod
    def get_method(cls) -> Methods:
        return Methods.GET

    async def get(self, request: HttpRequest, **kwargs) -> HttpResponse:
        return await self.run_with_exception_handling(AsyncAPIRequest(request), **kwargs)

    async def run(self, request: AsyncAPIRequest, **kwargs) -> JsonResponse:
        await self.check_permitted(request, **kwargs)
        objects = self.get_model_cls().objects
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
    @abstractmethod
    def get_model_cls(cls) -> Type[Model]:
        raise NotImplementedError()

    @classmethod
    async def filter_objects_by_request(cls, request: AsyncAPIRequest, objects: QuerySet, **kwargs) -> QuerySet:
        filters_dict = {}
        allowed_filters = cls.get_allowed_filters()

        for key, value in cls.get_params_from_request(request, 'filter', {}).items():
            if cls.does_key_exist_in_allowed_filters(key, allowed_filters):
                filters_dict[key] = value

        return objects.filter(**filters_dict)

    @classmethod
    @abstractmethod
    def get_allowed_filters(cls) -> set[str]:
        raise NotImplementedError()

    @classmethod
    def does_key_exist_in_allowed_filters(cls, key: str, allowed_filters: set[str]) -> bool:
        if key.endswith('__in'):
            key = key[:-4]
        return key in allowed_filters

    @classmethod
    async def order_objects_by_request(cls, request: AsyncAPIRequest, objects: QuerySet, **kwargs) -> QuerySet:
        order_by_list = []
        allowed_order_by = cls.get_allowed_order_by()

        for value in cls.get_params_from_request(request, 'order_by', []):
            if cls.does_key_exist_in_allowed_order_by(value, allowed_order_by):
                order_by_list.append(value)
        if not order_by_list:
            order_by_list = ['id']
        return objects.order_by(*order_by_list)

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
    @abstractmethod
    async def serialize_object(cls, request: AsyncAPIRequest, obj: Model, **kwargs) -> JSONType:
        raise NotImplementedError()

    @classmethod
    def get_correct_page(cls, total_amount: int, page: int, page_size: int) -> int:
        if page < 0:
            return 0
        if page * page_size > total_amount:
            return max(0, math.ceil(total_amount / page_size) - 1)
        return page
