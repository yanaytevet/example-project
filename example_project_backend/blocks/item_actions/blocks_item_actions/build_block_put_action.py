from typing import Self, TypedDict, NotRequired

from blocks.models import Block
from common.simple_rest.async_api_request import AsyncAPIRequest
from common.simple_rest.item_actions.base_put_action import BaseItemAction, T


class BuildBlockItemActionDataType(TypedDict):
    should_build: NotRequired[bool]


class BuildBlockItemAction(BaseItemAction[Block]):
    INPUT_DATA_TYPE = BuildBlockItemActionDataType

    def __init__(self, obj: Block, should_build: bool = True):
        super().__init__(obj)
        self.should_build = should_build

    @classmethod
    async def create_from_request_and_data(cls, request: AsyncAPIRequest, obj: T, data: BuildBlockItemActionDataType,
                                           **kwargs) -> Self:
        return cls(obj, should_build=data.get('should_build', True))

    async def run(self) -> None:
        if self.should_build:
            self.obj.a += ' build'
        else:
            self.obj.a += ' not build'
        await self.obj.asave()
