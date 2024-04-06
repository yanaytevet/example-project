from typing import Self, TypedDict, NotRequired

from example_app.models import ExampleModel
from common.simple_rest.async_api_request import AsyncAPIRequest
from common.simple_rest.item_actions.base_put_action import BaseItemAction


class ExampleActionModelItemActionDataType(TypedDict):
    a: NotRequired[int]


class ExampleActionModelItemAction(BaseItemAction[ExampleModel]):
    INPUT_DATA_TYPE = ExampleActionModelItemActionDataType

    def __init__(self, obj: ExampleModel):
        super().__init__(obj)

    @classmethod
    async def create_from_request_and_data(cls, request: AsyncAPIRequest, obj: ExampleModel,
                                           data: ExampleActionModelItemActionDataType,
                                           **kwargs) -> Self:
        return cls(obj)

    async def run(self) -> None:
        pass
