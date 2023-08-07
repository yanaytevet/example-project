from typing import Optional

from common.django_utils.serializers.serializer import Serializer
from common.time_utils import TimeUtils
from common.type_hints import JSONType
from experts.managers.anonymous_manager import AnonymousManager
from users.models import User, UserEvent
from users.models.organization import Organization
from users.serializers.user_event_serializer import UserEventSerializer


class ShortOrganizationForAdminSerializer(Serializer[Organization]):
    def inner_serialize(self, obj: Organization) -> Optional[JSONType]:
        new_data = AnonymousManager.create_serializer_data_is_anonymous_from_organization(self.data, organization=obj)

        events_query = UserEvent.objects.filter(user__organization=obj)
        latest_user_event = events_query.last() if events_query.exists() else None

        is_inactive = True
        if obj.last_sub_project_created_time:
            is_inactive = TimeUtils.timedelta_to_days(TimeUtils.now() - obj.last_sub_project_created_time) > 30
        res = {
            "id": obj.id,
            "logo_url": obj.logo_url,
            "name": AnonymousManager.get_organization_name(new_data, obj),
            "description": obj.description,
            "total_users_in_subscription": obj.total_users_in_subscription,
            "calls_done_in_subscription": obj.calls_done_in_subscription,
            "credits_used_in_subscription": obj.credits_used_in_subscription,
            "max_credits_in_subscription": obj.max_credits_in_subscription,
            "credits_left_in_subscription": obj.get_credits_left_in_subscription(),
            "subscription_start_date": TimeUtils.to_default_str(obj.subscription_start_date),
            "subscription_end_date": TimeUtils.to_default_str(obj.subscription_end_date),
            "is_anonymous": obj.is_anonymous,
            "is_restricted": obj.is_restricted,
            "restricted_reasons": obj.restricted_reasons_array,
            "allow_project_serial_number": obj.allow_project_serial_number,
            "questions_max_amount": obj.questions_max_amount,
            "users_count": self.get_users_count(obj),
            "last_sub_project_created_time": TimeUtils.to_default_str(obj.last_sub_project_created_time),
            "last_call_created_time": TimeUtils.to_default_str(obj.last_call_created_time),
            "latest_user_event": UserEventSerializer().serialize(latest_user_event) if latest_user_event else None,
            'is_inactive': is_inactive,
        }
        return res

    def get_users_count(self, org: Organization) -> int:
        return User.objects.filter(organization_id=org.id).count()
