from typing import TypedDict

from blocks.models import Circle
from common.simple_rest.serializers.serializer import Serializer


class ShortCircleForClientSerializerOutput(TypedDict):
    id: int


class ShortCircleForClientSerializer(Serializer[Circle]):
    def inner_serialize(self, obj: Circle) -> ShortCircleForClientSerializerOutput:
        return {
            'id': obj.id,
        }
