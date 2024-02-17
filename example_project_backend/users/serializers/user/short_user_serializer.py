from typing import TypedDict

from common.simple_rest.serializers.serializer import Serializer
from users.models import User


class ShortUserSerializerOutput(TypedDict):
    id: int
    username: str
    full_name: str
    is_admin: bool


class ShortUserSerializer(Serializer[User]):
    def inner_serialize(self, obj: User) -> ShortUserSerializerOutput:
        return {
            'id': obj.id,
            'username': obj.username,
            'full_name': obj.get_full_name(),
            'is_admin': obj.is_admin(),
        }
