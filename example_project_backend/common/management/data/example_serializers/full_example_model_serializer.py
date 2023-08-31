
from common.simple_rest.serializers.serializer import Serializer
from common.type_hints import OptionalJSONType
from example_app.models import ExampleModel


class FullExampleModelSerializer(Serializer[ExampleModel]):
    def inner_serialize(self, obj: ExampleModel) -> OptionalJSONType:
        return {
            'id': obj.id,
        }
