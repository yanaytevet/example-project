from typing import Optional

from common.django_utils.serializers.serializer import Serializer
from common.time_utils import TimeUtils
from common.type_hints import JSONType
from experts.managers.anonymous_manager import AnonymousManager
from experts.models import Project
from users.models import User
from users.models.organization import Organization
from users.serializers.short_team_serializer import ShortTeamSerializer


class OrganizationSerializer(Serializer[Organization]):
    def inner_serialize(self, obj: Organization) -> Optional[JSONType]:
        new_data = AnonymousManager.create_serializer_data_is_anonymous_from_organization(self.data, organization=obj)

        res = {
            "id": obj.id,
            "name": AnonymousManager.get_organization_name(new_data, obj),
            "description": AnonymousManager.get_organization_description(new_data, obj),
            "logo_url": AnonymousManager.get_organization_logo_url(new_data, obj),
            "calls_done_in_subscription": obj.calls_done_in_subscription,
            "credits_used_in_subscription": obj.credits_used_in_subscription,
            "max_credits_in_subscription": obj.max_credits_in_subscription,
            "credits_left_in_subscription": obj.get_credits_left_in_subscription(),
            "teams": ShortTeamSerializer(new_data).serialize_manager(obj.team_set),
            "subscription_start_date": TimeUtils.to_simple_str(obj.subscription_start_date),
            "subscription_end_date": TimeUtils.to_simple_str(obj.subscription_end_date),
            "users_count": self.get_users_count(obj),
            "total_users_in_subscription": obj.total_users_in_subscription,
            "total_projects": self.get_projects_count(obj),
            "allow_project_serial_number": obj.allow_project_serial_number,
            "allow_internal_search": obj.allow_internal_search,
            "allow_complex_project_interaction": obj.allow_complex_project_interaction,
        }
        return res

    def get_users_count(self, org: Organization) -> int:
        return User.objects.filter(organization_id=org.id).count()

    def get_projects_count(self, org: Organization) -> int:
        return Project.objects.filter(organization_id=org.id).count()
