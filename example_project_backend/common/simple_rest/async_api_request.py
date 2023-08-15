import asyncio
from asyncio import Future

from asgiref.sync import sync_to_async
from django.contrib.auth.models import User
from django.http import HttpRequest

from common.simple_rest.api_request import APIRequest


class AsyncAPIRequest(APIRequest):
    def __init__(self, original_request: HttpRequest):
        self.future_user: Future[User] = Future()
        super().__init__(original_request)

    def init_user(self) -> None:
        loop = asyncio.get_event_loop()
        loop.create_task(self.async_init_user())

    async def async_init_user(self) -> None:
        user = await self.async_get_user()
        self.future_user.set_result(user)
        self.user = user

    def set_in_session(self, key: str, value: str) -> None:
        self.original_request.session[key] = value

    async def async_set_in_session(self, key: str, value: any) -> None:
        sync_to_async(self.set_in_session)(key, value)

    async def async_set_as_other(self, is_as_other: bool) -> None:
        await self.async_set_in_session('as_other', is_as_other)

    def get_from_session(self, key: str) -> any:
        return self.original_request.session.get(key)

    async def async_get_from_session(self, key: str) -> any:
        return await sync_to_async(self.get_from_session)(key)

    async def async_get_as_other(self) -> bool:
        return await self.async_get_from_session('as_other')

    async def async_get_user(self) -> User:
        return await sync_to_async(self.get_user)()
