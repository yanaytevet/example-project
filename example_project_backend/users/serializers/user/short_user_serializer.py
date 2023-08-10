from common.simple_rest.serializers.serializer import Serializer
from common.type_hints import OptionalJSONType
from users.models import User


class ShortUserSerializer(Serializer[User]):
    def inner_serialize(self, obj: User) -> OptionalJSONType:
        return {
            'id': obj.id,
            'username': obj.username,
            'full_name': obj.get_full_name(),
            'is_admin': obj.is_admin(),
        }
