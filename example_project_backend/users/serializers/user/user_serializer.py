from ninja import Schema

from common.simple_api.serializers.serializer import Serializer
from users.models import User


class UserSchema(Schema):
    id: int
    username: str
    email: str | None
    first_name: str
    last_name: str
    pic_url: str | None
    full_name: str
    is_admin: bool
    initials: str
    permissions: list[str]


class UserSerializer(Serializer):
    async def inner_serialize(self, obj: User) -> UserSchema:
        return UserSchema(
            id=obj.id,
            username=obj.username,
            email=obj.email,
            first_name=obj.first_name,
            last_name=obj.last_name,
            pic_url=obj.pic_url,
            full_name=obj.get_full_name(),
            is_admin=obj.is_admin(),
            initials=obj.get_initials(),
            permissions=obj.permissions,
        )
