from typing import Any

from common.simple_rest.serializers.serializer import Serializer
from common.type_hints import OptionalJSONType


class EmptySerializer(Serializer):
    def inner_serialize(self, obj: Any) -> OptionalJSONType:
        return {}
