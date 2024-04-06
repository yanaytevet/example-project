from typing import TypedDict

from example_app.models import ExampleModel
from common.simple_rest.serializers.serializer import Serializer


class ExampleNameSerializerOutput(TypedDict):
    id: int


class ExampleNameSerializer(Serializer[ExampleModel]):
    def inner_serialize(self, obj: ExampleModel) -> ExampleNameSerializerOutput:
        return {
            'id': obj.id,
        }
