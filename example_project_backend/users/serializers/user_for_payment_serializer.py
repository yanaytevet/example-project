from typing import Optional

from calls.calls_managers.calls_fetcher_manager import CallsFetcherManager
from calls.models import Call
from calls.serializers.short_call_serializer import ShortCallSerializer
from common.django_utils.serializers.serializer import Serializer
from common.type_hints import JSONType
from finance.models import DonationOption
from finance.serializers.donation_option_serializer import DonationOptionSerializer
from users.models import User


class UserForPaymentSerializer(Serializer[User]):
    def inner_serialize(self, obj: User) -> Optional[JSONType]:
        person_info = obj.get_person_info()
        payment_info = obj.expert.get_payment_info()
        upcoming_calls = list(CallsFetcherManager().retrieve_calls_without_invoice_for_user(obj, Call.objects))

        return {
            "id": obj.id,
            "country": person_info.country,
            "address": person_info.address,
            "recipient_legal_address": person_info.recipient_legal_address,
            "region": person_info.region,
            "postal_code": person_info.postal_code,
            "city": person_info.city,
            "rate_amount": obj.expert.rate_amount,
            "name_for_payment": payment_info.name_for_payment,
            "payment_info_type": payment_info.payment_info_type,
            "payment_info_data": payment_info.payment_info_data,
            "calls_without_invoices": ShortCallSerializer(self.data).serialize_iterable(upcoming_calls),

            'donation_options': DonationOptionSerializer().serialize_manager(DonationOption.objects),
            'donation_data': payment_info.donation_data
        }
