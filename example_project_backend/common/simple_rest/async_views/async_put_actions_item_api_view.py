import asyncio
from abc import ABC, abstractmethod

from asgiref.sync import sync_to_async
from django.db.models import Model
from django.http import HttpRequest, JsonResponse, HttpResponse

from .async_api_view_component import AsyncAPIViewComponent
from .serialize_item_mixin import SerializeItemMixin
from ..async_api_request import AsyncAPIRequest
from ..enums.methods import Methods
from ..enums.status_code import StatusCode
from ..exceptions.rest_api_exception import RestAPIException
from ..item_actions.base_put_action import BaseItemAction


class AsyncPutActionsItemAPIView(SerializeItemMixin, AsyncAPIViewComponent, ABC):
    ACTION_FIELD = 'action'
    ACTION_DATA_FIELD = 'action_data'

    @classmethod
    def get_method(cls) -> Methods:
        return Methods.PUT

    async def put(self, request: HttpRequest, **kwargs) -> HttpResponse:
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

    async def run_action(self, request: AsyncAPIRequest, obj: Model, **kwargs) -> None:
        if self.ACTION_FIELD not in request.data:
            raise RestAPIException(
                status_code=StatusCode.HTTP_400_BAD_REQUEST,
                error_code='action_field_is_missing',
                message=f'"{self.ACTION_FIELD}" field is missing',
            )
        if self.ACTION_DATA_FIELD not in request.data:
            raise RestAPIException(
                status_code=StatusCode.HTTP_400_BAD_REQUEST,
                error_code='action_data_field_is_missing',
                message=f'"{self.ACTION_DATA_FIELD}" field is missing',
            )
        action = request.data[self.ACTION_FIELD]
        action_data = request.data[self.ACTION_DATA_FIELD]
        action_classes_by_name = await self.get_put_action_classes_by_name(request, obj, **kwargs)
        if action not in action_classes_by_name:
            raise RestAPIException(
                status_code=StatusCode.HTTP_400_BAD_REQUEST,
                error_code='action_function_is_not_implemented',
                message=f'action "{action}" is not implemented',
            )
        action_obj: BaseItemAction = await action_classes_by_name[action].create_from_request_and_data(
            request, obj, action_data, **kwargs)
        await action_obj.run()

    @classmethod
    @abstractmethod
    async def get_put_action_classes_by_name(cls, request: AsyncAPIRequest, obj: Model, **kwargs) \
            -> dict[str, type[BaseItemAction]]:
        raise NotImplementedError()

    @classmethod
    def get_actions_names(cls) -> list[str]:
        return []
