from blocks.models import Block
from common.simple_rest.serializers.serializer import Serializer, T
from common.type_hints import OptionalJSONType


class BlockSerializer(Serializer[Block]):
    def inner_serialize(self, obj: Block) -> OptionalJSONType:
        return {
            'id': obj.id,
            'a': obj.a,
            'b': obj.b,
            'c': obj.c,
            'block_type': obj.block_type,
        }
