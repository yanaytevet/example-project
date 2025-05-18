from ninja import Schema

from common.simple_api.serializers.serializer import Serializer
from users.models.email_address import EmailAddress


class EmailAddressSchema(Schema):
    id: int
    email: str
    is_primary: bool


class EmailAddressSerializer(Serializer):
    def inner_serialize(self, obj: EmailAddress) -> EmailAddressSchema:
        return EmailAddressSchema(
            id=obj.id,
            email=obj.address,
            is_primary=obj.is_primary_email
        )
