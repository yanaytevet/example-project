from django.contrib.auth import get_user
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from common.django_utils.api_checkers.admin_api_checker import AdminAPIChecker
from operations_tasks.managers.operation_tasks_retriever import OperationsTasksRetriever
from operations_tasks.models import OperationTask
from users.managers.systems_managers.system_status_manager import SystemStatusManager


class MyAdminDataView(APIView):
    def get(self, request: Request) -> Response:
        user = get_user(request)
        AdminAPIChecker().raise_exception_if_not_valid(user)

        objects = OperationTask.objects
        return Response({
            "operation_tasks_amount": OperationsTasksRetriever.get_user_open_unresolved_tasks(objects, user).count(),
            'system_alerts': SystemStatusManager().get_alerts(),
        }, status=status.HTTP_200_OK)
