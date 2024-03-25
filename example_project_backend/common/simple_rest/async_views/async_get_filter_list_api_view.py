from abc import ABC, abstractmethod
from typing import Type

from django.db.models import Model, QuerySet, Q
from django.http import HttpRequest, JsonResponse, HttpResponse

from common.type_hints import JSONType
from .async_api_view_component import AsyncAPIViewComponent
from ..async_api_request import AsyncAPIRequest
from ..enums.methods import Methods
from ..enums.status_code import StatusCode
from ..permissions_checkers.request_query_params_fields_checker import RequestQueryParamsFieldsAPIChecker


class AsyncGetFilterListAPIView(AsyncAPIViewComponent, ABC):
    DEFAULT_SEARCH_SIZE = 5

    @classmethod
    def get_method(cls) -> Methods:
        return Methods.GET

    async def get(self, request: HttpRequest, **kwargs) -> HttpResponse:
        return await self.run_with_exception_handling(AsyncAPIRequest(request), **kwargs)

    async def run(self, request: AsyncAPIRequest, **kwargs) -> JsonResponse:
        await self.check_permitted(request, **kwargs)
        objects = self.get_model_cls().objects
        objects = await self.filter_and_sort_objects_by_request(request, objects, **kwargs)
        data = await self.serialize_objects(request, objects, **kwargs)
        return JsonResponse(data, status=StatusCode.HTTP_200_OK, safe=False)

    @classmethod
    @abstractmethod
    async def check_permitted(cls, request: AsyncAPIRequest, **kwargs) -> None:
        raise NotImplementedError()

    @classmethod
    @abstractmethod
    def get_model_cls(cls) -> Type[Model]:
        raise NotImplementedError()

    @classmethod
    async def filter_and_sort_objects_by_request(cls, request: AsyncAPIRequest, objects: QuerySet, **kwargs) -> QuerySet:
        objects = await cls.custom_filter_objects_by_request(request, objects, **kwargs)
        await RequestQueryParamsFieldsAPIChecker(['filter_value']).async_raise_exception_if_not_valid(request)
        filter_value = request.query_params['filter_value']
        filters_query = Q()
        for field in cls.get_fields_to_filter_by():
            filters_query = filters_query | Q(**{f'{field}__icontains': filter_value})

        objects = objects.filter(filters_query).distinct()
        return objects.order_by(*cls.get_order_by_fields())

    @classmethod
    async def custom_filter_objects_by_request(cls, request: AsyncAPIRequest, objects: QuerySet, **kwargs) -> QuerySet:
        return objects

    @classmethod
    @abstractmethod
    def get_fields_to_filter_by(cls) -> list[str]:
        raise NotImplementedError()

    @classmethod
    def get_order_by_fields(cls) -> list[str]:
        return ['-id']

    @classmethod
    async def serialize_objects(cls, request: AsyncAPIRequest, objects: QuerySet, **kwargs) -> list[JSONType]:
        return [await cls.serialize_object(request, obj, **kwargs) async for obj in objects[0: cls.DEFAULT_SEARCH_SIZE]]

    @classmethod
    @abstractmethod
    async def serialize_object(cls, request: AsyncAPIRequest, obj: Model, **kwargs) -> JSONType:
        raise NotImplementedError()
