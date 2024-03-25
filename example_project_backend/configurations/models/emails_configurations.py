from django.db import models

from configurations.enums.emails_senders_types import EmailsSendersTypes
from configurations.enums.emails_validations_types import EmailsValidationsTypes
from configurations.enums.marketing_platforms_type import MarketingPlatformsTypes
from configurations.models.configurations import Configurations


class EmailsConfigurations(Configurations):
    list_display = ['id', 'email_sender_type', 'marketing_platform_type', 'send_emails', 'emails_for_testing',
                    'rnd_admin_emails']
    raw_id_fields = []

    email_sender_type = models.CharField(max_length=30, choices=EmailsSendersTypes.choices(),
                                         default=EmailsSendersTypes.NONE)
    email_sender_params = models.JSONField(default=dict, blank=True)

    marketing_platform_type = models.CharField(max_length=30, choices=MarketingPlatformsTypes.choices(),
                                               default=MarketingPlatformsTypes.NONE)
    marketing_platform_params = models.JSONField(default=dict, blank=True)

    email_validation_type = models.CharField(max_length=30, choices=EmailsValidationsTypes.choices(),
                                             default=EmailsValidationsTypes.NONE)
    email_validation_params = models.JSONField(default=dict, blank=True)

    send_emails = models.BooleanField(default=False, blank=True)
    emails_for_testing = models.JSONField(default=list, blank=True)
    rnd_admin_emails = models.JSONField(default=list, blank=True)

    contact_us_link = models.TextField(default='', blank=True)
    privacy_link = models.TextField(default='', blank=True)
