from common.simple_rest.serializers.serializer import Serializer
from common.time_utils import TimeUtils
from common.type_hints import OptionalJSONType
from users.models import UserEvent
from users.serializers.user.short_user_serializer import ShortUserSerializer


class UserEventSerializer(Serializer[UserEvent]):
    def inner_serialize(self, obj: UserEvent) -> OptionalJSONType:
        return {
            'name': obj.name,
            'tab_id': obj.tab_id,
            'attributes': obj.attributes,
            'creation_time': TimeUtils.to_default_str(obj.creation_time),
            'user': ShortUserSerializer().serialize(obj.user)
        }
