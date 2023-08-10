import pytz

from common.simple_rest.async_api_request import AsyncAPIRequest
from common.simple_rest.async_views.async_simple_get_api_view import AsyncSimpleGetAPIView
from common.type_hints import JSONType
from configurations.models import GUIConfigurations


class FullConfigurationsView(AsyncSimpleGetAPIView):
    @classmethod
    async def check_permitted(cls, request: AsyncAPIRequest, **kwargs) -> None:
        pass

    @classmethod
    async def get_data(cls, request: AsyncAPIRequest, **kwargs) -> JSONType:
        return {
            'timezones': pytz.all_timezones,
            'gui_configurations': GUIConfigurations.get_as_json(),
        }
