from common.simple_rest.serializers.serializer import Serializer
from common.type_hints import OptionalJSONType
from users.models.email_address import EmailAddress


class EmailAddressSerializer(Serializer[EmailAddress]):

    def inner_serialize(self, obj: EmailAddress) -> OptionalJSONType:
        return {
            'id': obj.id,
            'email': obj.address,
            'is_primary': obj.is_primary_email
        }
