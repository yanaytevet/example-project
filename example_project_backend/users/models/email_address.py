from __future__ import annotations
from typing import List, Optional

from django.db import models

from users.consts.bounce_status import BounceStatus
from users.consts.email_validation_status import EmailValidationStatus


class EmailAddress(models.Model):
    search_fields = ['address', 'bounce_status', 'email_validation_status', 'validation_status_description',
                     'is_primary_email']
    list_filter = []
    list_display = ['address', 'bounce_status', 'email_validation_status', 'validation_status_description',
                    'is_primary_email']

    address = models.CharField(max_length=300, primary_key=True)
    bounce_status = models.CharField(max_length=120, default=BounceStatus.NO_BOUNCE, blank=True)
    email_validation_status = models.CharField(max_length=120, choices=EmailValidationStatus.choices(),
                                               default=EmailValidationStatus.NOT_CHECKED, blank=True)
    validation_status_description = models.TextField(default=str, blank=True)
    is_primary_email = models.BooleanField(default=False, blank=True)

    def set_is_primary_email(self, is_primary: bool):
        self.is_primary_email = is_primary

    @classmethod
    def get_or_create_email_obj_by_address(cls, email_address: str) -> Optional[EmailAddress]:
        obj, _ = cls.objects.get_or_create(address=email_address)
        return obj

    @classmethod
    def get_all_email_obj_by_address(cls, email_addresses: List[str]) -> List[EmailAddress]:
        email_obj = [cls.get_or_create_email_obj_by_address(email_address) for email_address in email_addresses]
        email_obj_not_none = [email for email in email_obj if email]
        return email_obj_not_none
