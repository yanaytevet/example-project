from typing import Optional

from common.django_utils.serializers.serializer import Serializer
from common.type_hints import JSONType
from users.models.email_address import EmailAddress


class EmailAddressSerializer(Serializer[EmailAddress]):

    def inner_serialize(self, obj: EmailAddress) -> Optional[JSONType]:
        return {
            "email": obj.address,
            "is_primary": obj.is_primary_email
        }
