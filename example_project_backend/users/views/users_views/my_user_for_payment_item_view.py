from typing import Set

from rest_framework.exceptions import MethodNotAllowed
from rest_framework.request import Request

from common.consts.viewer_types import ViewerTypes
from common.django_utils.api_checkers.expert_api_checker import ExpertAPIChecker
from common.django_utils.rest_utils import BaseAPIItemView
from common.django_utils.serializers.serializer import Serializer
from users.models import User
from users.serializers.user_for_payment_serializer import UserForPaymentSerializer


class MyUserForPaymentItemView(BaseAPIItemView):

    @classmethod
    def get_item_serializer(cls) -> Serializer:
        return UserForPaymentSerializer()

    @classmethod
    def get_viewer_type(cls, user: User) -> ViewerTypes:
        return ViewerTypes.EXPERT

    @classmethod
    def get_update_allowed_attributes_set(cls) -> Set[str]:
        return set()

    @classmethod
    def is_allowed_put_update(cls) -> bool:
        return True

    @classmethod
    def get_obj(cls, request: Request, user: User) -> User:
        return user

    @classmethod
    def check_permitted_any_request_before_obj(cls, request: Request, user: User) -> None:
        ExpertAPIChecker().raise_exception_if_not_valid(user)

    def put_update(self, request: Request, user: User, obj: User) -> None:
        person_info = obj.get_person_info()
        payment_info = obj.expert.get_payment_info()

        for field in ['country', 'address', 'city', 'region', 'postal_code', 'recipient_legal_address']:
            value = request.data.get(field)
            if value is not None:
                setattr(person_info, field, value)

        for field in ['name_for_payment', 'payment_info_type', 'payment_info_data', 'donation_data', 'is_valid']:
            value = request.data.get(field)
            if value is not None:
                setattr(payment_info, field, value)

        obj.save()
        payment_info.save()

    @classmethod
    def check_permitted_delete_request_before_obj(cls, request: Request, user: User) -> None:
        raise MethodNotAllowed("DELETE")


    def put_update_rate_and_donation(self, request: Request, user: User, obj: User) -> None:
        rate_amount = request.data["rate_amount"]
        donation_data = request.data.get("donation_data")
        obj.expert.rate_amount = rate_amount
        obj.expert.donation_data = donation_data
        obj.expert.save()
