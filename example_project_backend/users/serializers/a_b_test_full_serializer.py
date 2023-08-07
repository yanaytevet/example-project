from typing import Optional

from common.django_utils.serializers.serializer import Serializer
from common.time_utils import TimeUtils
from common.type_hints import JSONType
from experts.managers.statistics_manager.a_b_statistics_manager import ABStatisticsManager
from users.models import ABTest


class ABTestFullSerializer(Serializer[ABTest]):
    def inner_serialize(self, obj: ABTest) -> Optional[JSONType]:
        ab_statistics_manager = ABStatisticsManager(obj.start_time, obj.end_time)
        return {
            'id': obj.id,
            'name': obj.name,
            'description': obj.description,
            'start_time': TimeUtils.to_default_str(obj.start_time),
            'end_time': TimeUtils.to_default_str(obj.end_time),
            'status': obj.get_status(),
            'onboarding_statistics': ab_statistics_manager.get_onboarding_status_survival(),
        }
