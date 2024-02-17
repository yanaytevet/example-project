from blocks.models import Block
from common.simple_rest.serializers.serializer import Serializer, T
from common.type_hints import OptionalJSONType


class FullOtherBlockSerializer(Serializer[Block]):
    def inner_serialize(self, obj: Block) -> OptionalJSONType:
        return {
            'id': obj.id,
            'a': obj.a,
            'c': obj.c,
            'block_type': obj.block_type,
            'another_field': 'another_value'
        }
