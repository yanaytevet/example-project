from typing import Optional

from common.django_utils.serializers.serializer import Serializer
from common.type_hints import JSONType
from experts.managers.anonymous_manager import AnonymousManager
from users.models import Team


class ShortTeamSerializer(Serializer[Team]):
    def inner_serialize(self, obj: Team) -> Optional[JSONType]:
        new_data = AnonymousManager.create_serializer_data_is_anonymous_from_team(self.data, team=obj)
        return {
            "id": obj.id,
            "name": AnonymousManager.get_team_name(new_data, obj),
        }
