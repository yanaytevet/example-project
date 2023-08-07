from django.contrib.auth import get_user
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from common.django_utils.api_checkers.finance_admin_api_checker import FinanceAdminAPIChecker
from common.django_utils.api_checkers.request_data_fields_api_checker import RequestDataFieldsAPIChecker
from common.time_utils import TimeUtils
from users.managers.timelines.timelines_groups_creator import TimelinesGroupsCreator
from users.models import User


class TimelinesByAdminView(APIView):
    def post(self, request: Request) -> Response:
        user = get_user(request)
        FinanceAdminAPIChecker().raise_exception_if_not_valid(user)
        RequestDataFieldsAPIChecker(['users_ids', 'start_time', 'end_time']).raise_exception_if_not_valid(request)
        start_time_str = request.data['start_time']
        start_time = TimeUtils.from_default_str(start_time_str)
        end_time_str = request.data['end_time']
        end_time = TimeUtils.from_default_str(end_time_str)
        users_ids = request.data['users_ids']
        users = [User.objects.get(id=user_id) for user_id in users_ids]
        timelines_group_creator = TimelinesGroupsCreator(users, start_time, end_time)
        return Response(timelines_group_creator.generate_timelines(), status=status.HTTP_200_OK)
