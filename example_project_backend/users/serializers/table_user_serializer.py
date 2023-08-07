from typing import Optional

from common.django_utils.serializers.serializer import Serializer
from common.time_utils import TimeUtils
from common.type_hints import JSONType
from experts.managers.anonymous_manager import AnonymousManager
from users.models import User, UserEvent
from users.serializers.short_team_serializer import ShortTeamSerializer
from users.serializers.user_event_serializer import UserEventSerializer


class TableUserSerializer(Serializer[User]):
    def inner_serialize(self, obj: User) -> Optional[JSONType]:
        person_info = obj.get_person_info()
        events_query = UserEvent.objects.filter(user=obj)
        latest_user_event = events_query.last() if events_query.exists() else None

        is_inactive = True
        if obj.last_sub_project_created_time:
            is_inactive = TimeUtils.timedelta_to_days(TimeUtils.now() - obj.last_sub_project_created_time) > 30
        return {
            "id": obj.id,
            "username": AnonymousManager.anonymize_string(self.data, obj.username),
            "email": AnonymousManager.anonymize_string(self.data, person_info.get_primary_email()),
            "first_name": AnonymousManager.anonymize_string(self.data, person_info.first_name),
            "last_name": AnonymousManager.anonymize_string(self.data, person_info.last_name),
            "teams": ShortTeamSerializer(self.data).serialize_manager(obj.get_teams()),
            "full_name": AnonymousManager.get_client_name(self.data, obj),
            "is_org_manager": obj.is_org_manager(),
            "last_sub_project_created_time": TimeUtils.to_default_str(obj.last_sub_project_created_time),
            "last_call_created_time": TimeUtils.to_default_str(obj.last_call_created_time),
            "latest_user_event": UserEventSerializer().serialize(latest_user_event) if latest_user_event else None,
            'is_inactive': is_inactive,
        }
