from typing import Set, Type

from django.db.models import Model
from rest_framework.request import Request

from common.consts.viewer_types import ViewerTypes
from common.django_utils.api_checkers.org_manager_api_checker import OrgManagerAPIChecker
from common.django_utils.rest_utils import BaseAPIItemByIdView
from common.django_utils.serializers.serializer import Serializer
from users.apis_checkers.users_api_checkers import UserBelongToOrgAPIChecker
from users.models import User, UserEvent
from users.serializers.user.user_serializer import UserSerializer
from users.users_actions.general_users_actions import GeneralUsersActions
from users.views.users_views.user_item_mixin import UserItemMixin


class UserItemByManagerView(BaseAPIItemByIdView, UserItemMixin):

    @classmethod
    def get_model_cls(cls) -> Type[Model]:
        return User

    @classmethod
    def get_item_serializer(cls) -> Serializer:
        return UserSerializer()

    @classmethod
    def get_viewer_type(cls, user: User) -> ViewerTypes:
        return ViewerTypes.CLIENT

    @classmethod
    def get_update_allowed_attributes_set(cls) -> Set[str]:
        return {'first_name', 'last_name', 'teams'}

    @classmethod
    def is_allowed_put_update(cls) -> bool:
        return True

    @classmethod
    def check_permitted_any_request_before_obj(cls, request: Request, user: User) -> None:
        OrgManagerAPIChecker().raise_exception_if_not_valid(user)

    @classmethod
    def check_permitted_any_request_after_obj(cls, request: Request, user: User, obj: User) -> None:
        UserBelongToOrgAPIChecker().raise_exception_if_not_valid(obj, user.organization)

    @classmethod
    def run_before_delete(cls, request: Request, user: User, obj: User) -> None:
        obj.get_person_info().delete()

    def put_change_password(self, request: Request, user: User, obj: User) -> None:
        new_password = request.data['new_password']
        GeneralUsersActions().change_password_by_org_manager(obj, org_manager=user, password=new_password)
        UserEvent(name='org_manager_change_other_password', user=user, attributes={'user_id': obj.id}).save()

    def put_update(self, request: Request, user: User, obj: User) -> None:
        person_info = obj.get_person_info()

        first_name = request.data.get('first_name')
        if first_name:
            person_info.first_name = first_name

        last_name = request.data.get('last_name')
        if last_name:
            person_info.last_name = last_name

        obj.save()

        teams_ids = request.data.get('teams_ids')
        if teams_ids is not None:
            obj.teams.clear()
            for team_id in teams_ids:
                obj.teams.add(team_id)

