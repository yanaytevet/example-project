from typing import Self

from example_app.models import ExampleModel
from common.simple_rest.async_api_request import AsyncAPIRequest
from common.simple_rest.item_actions.base_put_action import BaseItemAction, T
from common.type_hints import JSONType


class DoStuffExampleModelItemAction(BaseItemAction[ExampleModel]):
    @classmethod
    async def create_from_request_and_data(cls, request: AsyncAPIRequest, obj: ExampleModel, data: JSONType, **kwargs) \
            -> Self:
        return cls(obj)

    async def run(self) -> None:
        pass
