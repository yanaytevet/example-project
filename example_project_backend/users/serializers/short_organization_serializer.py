from typing import Optional

from common.django_utils.serializers.serializer import Serializer
from common.type_hints import JSONType
from experts.managers.anonymous_manager import AnonymousManager
from users.models.organization import Organization


class ShortOrganizationSerializer(Serializer[Organization]):
    def inner_serialize(self, obj: Organization) -> Optional[JSONType]:
        new_data = AnonymousManager.create_serializer_data_is_anonymous_from_organization(self.data, organization=obj)
            
        res = {
            "id": obj.id,
            "name": AnonymousManager.get_organization_name(new_data, obj),
            "calls_done_in_subscription": obj.calls_done_in_subscription,
            "credits_used_in_subscription": obj.credits_used_in_subscription,
            "max_credits_in_subscription": obj.max_credits_in_subscription,
            "credits_left_in_subscription": obj.get_credits_left_in_subscription(),
            "questions_max_amount": obj.questions_max_amount or Organization.DEFAULT_QUESTIONS_MAX_AMOUNT,
            "can_make_more_calls": obj.can_make_more_calls(),
            "allow_complex_project_interaction": obj.allow_complex_project_interaction,
        }
        return res
