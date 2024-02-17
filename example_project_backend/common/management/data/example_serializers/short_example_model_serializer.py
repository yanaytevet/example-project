from typing import TypedDict

from example_app.models import ExampleModel

from common.simple_rest.serializers.serializer import Serializer


class ShortExampleModelSerializerOutput(TypedDict):
    id: int


class ShortExampleModelSerializer(Serializer[ExampleModel]):
    def inner_serialize(self, obj: ExampleModel) -> ShortExampleModelSerializerOutput:
        return {
            'id': obj.id,
        }
