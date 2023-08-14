from common.simple_rest.serializers.serializer import Serializer
from common.type_hints import OptionalJSONType
from users.managers.emails_managers.user_emails_manager import UserEmailsManager
from users.models import User


class UserSerializer(Serializer[User]):
    def inner_serialize(self, obj: User) -> OptionalJSONType:
        return {
            'id': obj.id,
            'username': obj.username,
            'email': UserEmailsManager(obj).get_primary_email(),
            'first_name': obj.first_name,
            'last_name': obj.last_name,
            'pic_url': obj.pic_url,
            'full_name': obj.get_full_name(),
            'is_admin': obj.is_admin(),
            'permissions': obj.permissions,
        }
