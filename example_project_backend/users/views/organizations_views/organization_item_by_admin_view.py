from typing import Set, Type

from django.db.models import Model
from rest_framework.request import Request

from common.consts.viewer_types import ViewerTypes
from common.django_utils.api_checkers.admin_api_checker import AdminAPIChecker
from common.django_utils.api_checkers.request_data_fields_api_checker import RequestDataFieldsAPIChecker
from common.django_utils.rest_utils import BaseAPIItemByIdView
from common.django_utils.serializers.serializer import Serializer
from experts.managers.projects_manager.demo_project_manager import DemoProjectManager
from experts.models import Project
from users.managers.organization_calculator import OrganizationCalculator
from users.models import User, Organization
from users.serializers.short_organization_for_admin_serializer import ShortOrganizationForAdminSerializer


class OrganizationItemByAdminView(BaseAPIItemByIdView):

    @classmethod
    def get_model_cls(cls) -> Type[Model]:
        return Organization

    @classmethod
    def get_item_serializer(cls) -> Serializer:
        return ShortOrganizationForAdminSerializer()

    @classmethod
    def get_viewer_type(cls, user: User) -> ViewerTypes:
        return ViewerTypes.ADMIN

    @classmethod
    def get_update_allowed_attributes_set(cls) -> Set[str]:
        return {"name", 'description', 'is_anonymous', 'allow_project_serial_number', 'questions_max_amount',
                'allow_internal_search'}

    @classmethod
    def is_allowed_put_update(cls) -> bool:
        return True

    def put_add_demo_project(self, request: Request, user: User, obj: Organization) -> None:
        RequestDataFieldsAPIChecker(['project_id']).raise_exception_if_not_valid(request=request)
        project_id = request.data['project_id']
        project = Project.objects.get(id=project_id)
        DemoProjectManager().create_demo(obj, project)

    def put_recalc_calls(self, request: Request, user: User, obj: Organization) -> None:
        OrganizationCalculator(obj).recalc_calls()

    @classmethod
    def check_permitted_any_request_before_obj(cls, request: Request, user: User) -> None:
        AdminAPIChecker().raise_exception_if_not_valid(user)

    def put_update_restricted_reasons(self, request: Request, user: User, obj: Organization) -> None:
        RequestDataFieldsAPIChecker(['restricted_reasons']).raise_exception_if_not_valid(request=request)
        restricted_reasons = request.data['restricted_reasons']
        obj.set_restricted_reasons(restricted_reasons)
        obj.save()
