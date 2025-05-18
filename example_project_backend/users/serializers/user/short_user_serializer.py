from typing import TypedDict

from ninja import Schema

from common.simple_api.serializers.serializer import Serializer
from users.models import User


class ShortUserOutput(Schema):
    id: int
    username: str
    full_name: str
    is_admin: bool


class ShortUserSerializer(Serializer):
    def inner_serialize(self, obj: User) -> ShortUserOutput:
        return ShortUserOutput(
            id=obj.id,
            username=obj.username,
            full_name=obj.get_full_name(),
            is_admin=obj.is_admin(),
        )
