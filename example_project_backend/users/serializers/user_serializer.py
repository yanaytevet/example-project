from typing import Optional

from common.django_utils.serializers.serializer import Serializer
from common.type_hints import JSONType
from experts.managers.anonymous_manager import AnonymousManager
from users.managers.persona_manager import PersonaManager
from users.models import User
from users.serializers.persona_serializer import PersonaSerializer
from users.serializers.short_organization_serializer import ShortOrganizationSerializer
from users.serializers.short_team_serializer import ShortTeamSerializer


class UserSerializer(Serializer[User]):
    def inner_serialize(self, obj: User) -> Optional[JSONType]:
        person_info = obj.get_person_info()
        persona = PersonaManager.get_persona_by_user(obj)

        return {
            "id": obj.id,
            "username": AnonymousManager.anonymize_string(self.data, obj.username),
            "email": AnonymousManager.anonymize_string(self.data, person_info.get_primary_email()),
            "preferred_language": obj.preferred_language,
            "pic_url": AnonymousManager.anonymize_string(self.data, obj.pic_url),
            "first_name": AnonymousManager.anonymize_string(self.data, person_info.first_name),
            "last_name": AnonymousManager.anonymize_string(self.data, person_info.last_name),
            "full_name": AnonymousManager.get_client_name(self.data, obj),
            "is_client": obj.organization is not None,
            "is_expert": obj.is_expert(),
            "is_org_manager": obj.is_org_manager(),
            "is_admin": obj.is_admin(),
            "is_finance_admin": obj.is_finance_admin(),
            "is_template_admin":obj.is_template_admin(),
            "teams": ShortTeamSerializer(self.data).serialize_manager(obj.get_teams()),
            "organization": ShortOrganizationSerializer(self.data).serialize(obj.organization),
            "permissions": obj.permissions_array,
            "a_b_group": person_info.a_b_group,
            "contact_persona": PersonaSerializer(self.data).serialize(persona)
        }
