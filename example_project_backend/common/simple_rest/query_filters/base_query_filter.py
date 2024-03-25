from abc import ABC, abstractmethod
from typing import TypeVar, Generic, Self

from django.db.models import QuerySet

from common.simple_rest.async_api_request import AsyncAPIRequest
from common.type_hints import JSONType

T = TypeVar('T')


class BaseQueryFilter(ABC, Generic[T]):

    @abstractmethod
    async def run(self, query: QuerySet[T]) -> QuerySet[T]:
        raise NotImplementedError()

    @classmethod
    @abstractmethod
    async def create_from_request_and_data(cls, request: AsyncAPIRequest, data: JSONType, **kwargs) -> Self:
        raise NotImplementedError()
