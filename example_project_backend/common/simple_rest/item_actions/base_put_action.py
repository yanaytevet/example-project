from abc import ABC, abstractmethod
from typing import Generic, TypeVar, Self

from common.simple_rest.async_api_request import AsyncAPIRequest
from common.type_hints import JSONType

T = TypeVar('T')


class BaseItemAction(ABC, Generic[T]):
    def __init__(self, obj: T):
        self.obj = obj

    @abstractmethod
    async def run(self) -> None:
        raise NotImplementedError()

    @classmethod
    @abstractmethod
    async def create_from_request_and_data(cls, request: AsyncAPIRequest, obj: T, data: JSONType, **kwargs) -> Self:
        raise NotImplementedError()
