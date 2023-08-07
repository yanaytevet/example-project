from typing import Optional

from common.django_utils.serializers.serializer import Serializer
from common.type_hints import JSONType
from users.models import Persona


class PersonaSerializer(Serializer[Persona]):
    def inner_serialize(self, obj: Persona) -> Optional[JSONType]:
        return {
            'id': obj.id,
            'full_name': obj.get_full_name(),
            'first_name': obj.first_name,
            'last_name': obj.last_name,
            'email': obj.email,
        }
