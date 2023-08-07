from typing import Optional

from common.django_utils.serializers.serializer import Serializer
from common.type_hints import JSONType
from experts.managers.anonymous_manager import AnonymousManager
from users.models import User
from users.serializers.short_team_serializer import ShortTeamSerializer


class ShortUserSerializer(Serializer[User]):
    def inner_serialize(self, obj: User) -> Optional[JSONType]:
        person_info = obj.get_person_info()
        return {
            "id": obj.id,
            "username": AnonymousManager.anonymize_string(self.data, obj.username),
            "email": AnonymousManager.anonymize_string(self.data, person_info.get_primary_email()),
            "first_name": AnonymousManager.anonymize_string(self.data, person_info.first_name),
            "last_name": AnonymousManager.anonymize_string(self.data, person_info.last_name),
            "pic_url": AnonymousManager.anonymize_string(self.data, obj.pic_url),
            "teams": ShortTeamSerializer(self.data).serialize_manager(obj.get_teams()),
            "full_name": AnonymousManager.get_user_full_name(self.data, obj),
            "is_org_manager": obj.is_org_manager(),
            "is_admin": obj.is_admin(),
            "is_client": obj.is_client(),
            "is_expert": obj.is_expert(),
        }
