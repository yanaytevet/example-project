from typing import Set, Type

from django.db.models import Model
from rest_framework.request import Request

from common.consts.viewer_types import ViewerTypes
from common.django_utils.api_checkers.admin_api_checker import AdminAPIChecker
from common.django_utils.rest_utils import BaseAPIItemByIdView
from common.django_utils.serializers.serializer import Serializer
from users.models import User
from users.serializers.user_serializer import UserSerializer
from users.users_actions.general_users_actions import GeneralUsersActions
from users.views.users_views.user_item_mixin import UserItemMixin


class UserItemByAdminView(BaseAPIItemByIdView, UserItemMixin):

    @classmethod
    def get_model_cls(cls) -> Type[Model]:
        return User

    @classmethod
    def get_item_serializer(cls) -> Serializer:
        return UserSerializer()

    @classmethod
    def get_viewer_type(cls, user: User) -> ViewerTypes:
        return ViewerTypes.ADMIN

    @classmethod
    def get_update_allowed_attributes_set(cls) -> Set[str]:
        return {"first_name", "last_name", "teams"}

    @classmethod
    def is_allowed_put_update(cls) -> bool:
        return True

    @classmethod
    def check_permitted_any_request_before_obj(cls, request: Request, user: User) -> None:
        AdminAPIChecker().raise_exception_if_not_valid(user)

    def put_change_password(self, request: Request, user: User, obj: User) -> None:
        new_password = request.data["new_password"]
        GeneralUsersActions().change_password_by_admin(obj, admin=user, password=new_password)
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


