from asgiref.sync import sync_to_async
from django.contrib.auth import authenticate, login, logout

from common.simple_api.api_request import APIRequest
from users.models import User

# def jwt_auth(self, request: Request) -> dict:
#     token = request.META.get('HTTP_AUTHORIZATION', ' ').split(' ')[1]
#     secret = AuthKeyConfigurations.get().auth_jwt_key
#     payload = jwt.decode(token, secret, algorithms=['HS256'])
#     return payload


class DjangoAuth:
    @classmethod
    def authenticate(cls, request: APIRequest, username: str, password: str) -> User:
        return authenticate(request.original_request, username=username, password=password)

    @classmethod
    async def async_authenticate(cls, request: APIRequest, username: str, password: str) -> User:
        return await sync_to_async(cls.authenticate)(request, username, password)

    @classmethod
    def login(cls, request: APIRequest, user: User) -> User:
        return login(request.original_request, user)

    @classmethod
    async def async_login(cls, request: APIRequest, user: User) -> User:
        return await sync_to_async(cls.login)(request, user)

    @classmethod
    def logout(cls, request: APIRequest) -> None:
        logout(request.original_request)

    @classmethod
    async def async_logout(cls, request: APIRequest) -> None:
        await sync_to_async(cls.logout)(request)
