import pytz
from rest_framework.request import Request

from common.django_utils.api_checkers.request_data_fields_api_checker import RequestDataFieldsAPIChecker
from users.models import PersonInfo


class TimeZoneManager:
    def __init__(self, person_info: PersonInfo):
        self.person_info = person_info

    def update_by_request(self, request: Request) -> None:
        if self.person_info.preferred_timezone_offset != 'UTC':
            return
        RequestDataFieldsAPIChecker(['timezone_name']).raise_exception_if_not_valid(request=request)
        timezone_name = request.data['timezone_name']
        if timezone_name in pytz.all_timezones_set:
            self.person_info.preferred_timezone_offset = timezone_name
            self.person_info.save()
