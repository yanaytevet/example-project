from typing import Type

import pytz
from ninja import Schema, Path, Query

from common.simple_api.api_request import APIRequest
from common.simple_api.views.simple_get_api_view import SimpleGetAPIView


class FullConfigurationsOutput(Schema):
    timezones: list[str]


class FullConfigurationsView(SimpleGetAPIView):
    @classmethod
    def get_output_schema(cls) -> Type[Schema]:
        return FullConfigurationsOutput

    @classmethod
    async def check_permitted(cls, api_request: APIRequest, query: Query = None, path: Path = None) -> None:
        pass

    @classmethod
    async def get_data(cls, api_request: APIRequest, query: Query = None, path: Path = None
                       ) -> FullConfigurationsOutput:
        return FullConfigurationsOutput(
            timezones=list(pytz.all_timezones),
        )
