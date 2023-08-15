from abc import abstractmethod

from django.http import HttpResponse, HttpRequest, JsonResponse

from common.simple_rest.async_api_request import AsyncAPIRequest
from common.simple_rest.async_views.async_api_view_component import AsyncAPIViewComponent
from common.simple_rest.constants.methods import Methods
from common.simple_rest.constants.status_code import StatusCode
from configurations.models.demo import Demo


class DemoView(AsyncAPIViewComponent):
    @classmethod
    def get_method(cls) -> Methods:
        return Methods.GET

    async def get(self, request: HttpRequest, **kwargs) -> HttpResponse:
        return await self.run_with_exception_handling(AsyncAPIRequest(request), **kwargs)

    async def run(self, request: AsyncAPIRequest, **kwargs) -> HttpResponse:
        user = await request.future_user
        self.check_permitted(request, user)
        demo = self.get_demo_object()
        return JsonResponse(demo.data, status=StatusCode.HTTP_200_OK)

    @abstractmethod
    def get_demo_key(self) -> str:
        raise NotImplementedError()

    def get_demo_object(self) -> Demo:
        return Demo.objects.filter(key=self.get_demo_key()).first()
