from typing import TypedDict

from example_app.models import ExampleModel

from common.simple_rest.serializers.serializer import Serializer


class FullExampleModelSerializerOutput(TypedDict):
    id: int


class FullExampleModelSerializer(Serializer[ExampleModel]):
    def inner_serialize(self, obj: ExampleModel) -> FullExampleModelSerializerOutput:
        return {
            'id': obj.id,
        }
