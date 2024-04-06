from typing import Self, TypedDict, NotRequired

from django.db.models import QuerySet
from example_app.models import ExampleModel
from common.simple_rest.async_api_request import AsyncAPIRequest
from common.simple_rest.query_filters.base_query_filter import BaseQueryFilter


class ExampleFilterModelQueryFilterDataType(TypedDict):
    a: NotRequired[int]


class ExampleFilterModelQueryFilter(BaseQueryFilter[ExampleModel]):
    INPUT_DATA_TYPE = ExampleFilterModelQueryFilterDataType

    async def run(self, query: QuerySet[ExampleModel]) -> QuerySet[ExampleModel]:
        return query

    @classmethod
    async def create_from_request_and_data(cls, request: AsyncAPIRequest,
                                           data: ExampleFilterModelQueryFilterDataType,
                                           **kwargs) -> Self:
        return cls()
