from typing import TypedDict

from blocks.models import Circle
from common.simple_rest.serializers.serializer import Serializer


class FullCircleForClientSerializerOutput(TypedDict):
    id: int


class FullCircleForClientSerializer(Serializer[Circle]):
    def inner_serialize(self, obj: Circle) -> FullCircleForClientSerializerOutput:
        return {
            'id': obj.id,
        }
