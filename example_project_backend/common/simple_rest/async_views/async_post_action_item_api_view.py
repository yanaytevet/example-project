from abc import ABC, abstractmethod

from django.db.models import Model
from django.http import HttpRequest, JsonResponse, HttpResponse

from common.type_hints import JSONType
from .async_api_view_component import AsyncAPIViewComponent
from .serialize_item_mixin import SerializeItemMixin
from ..async_api_request import AsyncAPIRequest
from ..enums.methods import Methods
from ..enums.status_code import StatusCode


class AsyncPostActionItemAPIView(SerializeItemMixin, AsyncAPIViewComponent, ABC):

    @classmethod
    def get_method(cls) -> Methods:
        return Methods.POST

    async def post(self, request: HttpRequest, **kwargs) -> HttpResponse:
        return await self.run_with_exception_handling(AsyncAPIRequest(request), **kwargs)

    async def run(self, request: AsyncAPIRequest, **kwargs) -> JsonResponse:
        await self.check_permitted_before_object(request, **kwargs)
        obj = await self.get_object(request, **kwargs)
        await self.check_permitted_after_object(request, obj, **kwargs)
        await self.run_action(request, obj, **kwargs)
        data = await self.serialize_object(request, obj, **kwargs)
        return JsonResponse(data, status=StatusCode.HTTP_200_OK)

    @classmethod
    @abstractmethod
    async def check_permitted_before_object(cls, request: AsyncAPIRequest, **kwargs) -> None:
        raise NotImplementedError()

    @classmethod
    @abstractmethod
    async def get_object(cls, request: AsyncAPIRequest, **kwargs) -> Model:
        raise NotImplementedError()

    @classmethod
    @abstractmethod
    async def check_permitted_after_object(cls, request: AsyncAPIRequest,  obj: Model, **kwargs) -> None:
        raise NotImplementedError()

    @classmethod
    @abstractmethod
    async def run_action(cls, request: AsyncAPIRequest, obj: Model, **kwargs) -> JSONType:
        raise NotImplementedError()

