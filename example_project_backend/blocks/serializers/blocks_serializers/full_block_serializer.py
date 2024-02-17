from typing import TypedDict

from blocks.consts.block_types import BlockTypes
from blocks.models import Block
from common.simple_rest.serializers.serializer import Serializer
from users.serializers.user.short_user_serializer import ShortUserSerializerOutput


class FullBlockSerializerOutput(TypedDict):
    id: int
    a: str
    b: int
    c: bool
    block_type: BlockTypes
    another_field: str
    user: ShortUserSerializerOutput


class FullBlockSerializer(Serializer[Block]):
    def inner_serialize(self, obj: Block) -> FullBlockSerializerOutput:
        return {
            'id': obj.id,
            'a': obj.a,
            'b': obj.b,
            'c': obj.c,
            'block_type': obj.block_type,
            'another_field': 'another_value'
        }
