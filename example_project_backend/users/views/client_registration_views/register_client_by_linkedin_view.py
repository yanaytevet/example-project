from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from experts.apis_checkers.experts_api_checkers import ExpertSecretIdAPIChecker
from experts.consts.workflow_enum import ExpertWorkflowEventTrigger
from experts.managers.expert_workflow_event_manager.expert_workflow_event_manager import ExpertWorkflowEventManager
from experts.models import Expert


class RegisterClientByLinkedinView(APIView):
    def post(self, request: Request) -> Response:
        expert = Expert.objects.filter(id=request.data['expert_id']).first()
        ExpertSecretIdAPIChecker().raise_exception_if_not_valid(expert, request.data['secret_id'])
        ExpertWorkflowEventManager().handle_situation(ExpertWorkflowEventTrigger.START_LINKEDIN_REGISTRATION, expert)
        return Response(None, status=status.HTTP_200_OK)

