from common.simple_rest.serializers.serializer import Serializer
from common.type_hints import OptionalJSONType
from configurations.models.demo import Demo


class DemoSerializer(Serializer[Demo]):
    def inner_serialize(self, obj: Demo) -> OptionalJSONType:
        return {
            'id': obj.id,
            'data': obj.data,
            'key': obj.key,
            'name_hash': obj.name_hash,
        }
