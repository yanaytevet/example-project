from typing import Set

from rest_framework.exceptions import MethodNotAllowed
from rest_framework.request import Request

from common.django_utils.api_checkers.login_api_checker import LoginAPIChecker
from common.django_utils.api_checkers.request_data_fields_api_checker import RequestDataFieldsAPIChecker
from common.django_utils.rest_utils import BaseAPIItemView
from common.django_utils.serializers.serializer import Serializer
from emails.marketing_emails.marketing_lists_updater_generator import MarketingListsUpdaterGenerator
from experts.consts.experts_status import ExpertStatus
from users.consts.push_notifications_status import PushNotificationsStatus
from users.models import User
from users.serializers.full_user_serializer import FullUserSerializer


class MyFullUserItemView(BaseAPIItemView):

    @classmethod
    def get_item_serializer(cls) -> Serializer:
        return FullUserSerializer()

    @classmethod
    def get_update_allowed_attributes_set(cls) -> Set[str]:
        return {'preferred_timezone_offset', 'country', 'address', 'region', 'city', 'postal_code'}

    @classmethod
    def is_allowed_put_update(cls) -> bool:
        return True

    @classmethod
    def get_obj(cls, request: Request, user: User) -> User:
        return user

    def put_update(self, request: Request, user: User, obj: User) -> None:
        super().put_update(request, user, obj.get_person_info())

    @classmethod
    def check_permitted_any_request_before_obj(cls, request: Request, user: User) -> None:
        LoginAPIChecker().raise_exception_if_not_valid(user)

    @classmethod
    def check_permitted_delete_request_before_obj(cls, request: Request, user: User) -> None:
        raise MethodNotAllowed("DELETE")

    def put_change_allowed_notification(self, request: Request, user: User, obj: User) -> None:
        RequestDataFieldsAPIChecker(['notifications_type', 'is_allowed']).raise_exception_if_not_valid(request=request)
        notifications_type = request.data['notifications_type']
        is_allowed = request.data['is_allowed']
        if is_allowed:
            obj.allowed_notifications_array.append(notifications_type)
        else:
            obj.allowed_notifications_array.remove(notifications_type)
        obj.save()

    def put_update_primary_phone_number(self, request: Request, user: User, obj: User) -> None:
        RequestDataFieldsAPIChecker(['phone_number']).raise_exception_if_not_valid(request=request)
        phone_number = request.data['phone_number']
        obj.replace_primary_phone_number(phone_number)
        obj.save()

    def put_update_push_notifications_params(self, request: Request, user: User, obj: User) -> None:
        RequestDataFieldsAPIChecker(['push_notifications_params']).raise_exception_if_not_valid(request=request)
        obj.push_notifications_params = request.data['push_notifications_params']
        obj.push_notifications_status = PushNotificationsStatus.ACCEPTED
        obj.save()

    def put_deny_push_notifications(self, request: Request, user: User, obj: User) -> None:
        obj.push_notifications_status = PushNotificationsStatus.DENIED
        obj.save()

    def put_set_is_unsubscribed(self, request: Request, user: User, obj: User) -> None:
        RequestDataFieldsAPIChecker(['is_unsubscribed']).raise_exception_if_not_valid(request=request)
        obj.set_is_unsubscribed(request.data['is_unsubscribed'])
        obj.save()
        if user.is_expert():
            MarketingListsUpdaterGenerator.update_expert(user.expert)
