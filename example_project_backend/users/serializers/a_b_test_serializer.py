from typing import Optional

from common.django_utils.serializers.serializer import Serializer
from common.time_utils import TimeUtils
from common.type_hints import JSONType
from users.models import ABTest


class ABTestSerializer(Serializer[ABTest]):
    def inner_serialize(self, obj: ABTest) -> Optional[JSONType]:
        return {
            'id': obj.id,
            'name': obj.name,
            'description': obj.description,
            'start_time': TimeUtils.to_default_str(obj.start_time),
            'end_time': TimeUtils.to_default_str(obj.end_time),
            'status': obj.get_status(),
        }
