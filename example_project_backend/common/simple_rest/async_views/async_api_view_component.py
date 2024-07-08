from abc import abstractmethod, ABC

from django.db.models import Model
from django.http import JsonResponse, HttpResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from common.simple_rest.async_api_request import AsyncAPIRequest
from common.simple_rest.enums.methods import Methods
from common.simple_rest.exceptions.rest_api_exception import RestAPIException
from common.simple_rest.serializers.serializer import Serializer


@method_decorator(csrf_exempt, name='dispatch')
class AsyncAPIViewComponent(View, ABC):
    @classmethod
    @abstractmethod
    def get_method(cls) -> Methods:
        raise NotImplementedError()

    @abstractmethod
    async def run(self, request: AsyncAPIRequest, **kwargs) -> HttpResponse:
        raise NotImplementedError()

    async def run_with_exception_handling(self, request: AsyncAPIRequest, **kwargs) -> HttpResponse:
        try:
            return await self.run(request, **kwargs)
        except RestAPIException as e:
            return JsonResponse({
                'detail': e.message,
                'error_code': e.error_code,
            }, status=e.status_code)

    @classmethod
    async def get_all_serializers_by_name(cls) -> dict[str, Serializer]:
        return {}
