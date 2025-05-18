from typing import TypedDict

from example_app.models import ExampleModel
from ninja import Schema

from common.simple_api.serializers.serializer import Serializer


class ExampleNameOutput(Schema):
    id: int


class ExampleNameSerializer(Serializer):
    def inner_serialize(self, obj: ExampleModel) -> ExampleNameOutput:
        return ExampleNameOutput(id=obj.id)
