from typing import Optional, List

from django.contrib import admin
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import QuerySet, Q

from common.db_utils.postgres_fields.array_field_with_choices import ArrayFieldWithChoices
from experts.consts.experts_status import ExpertStatus
from users.consts.email_source import EmailSource
from users.consts.notifications_types import NotificationsTypes
from users.consts.permissions import Permissions
from users.consts.push_notifications_status import PushNotificationsStatus
from users.models import Team, PersonInfo, EmailAddress
from users.models.organization import Organization


def create_default_notifications() -> list[NotificationsTypes]:
    return [
        NotificationsTypes.CALL_REMINDERS,
        NotificationsTypes.NEW_PROJECT,
        NotificationsTypes.EXPERTS_FOUND]


class User(AbstractUser):
    list_filter = []
    raw_id_fields = ['teams', 'organization', 'person_info', 'organization']

    permissions_array = ArrayFieldWithChoices(choices=Permissions.choices(), blank=True, default=list)
    teams = models.ManyToManyField(Team, blank=True)
    organization = models.ForeignKey(Organization, blank=True, null=True, on_delete=models.SET_NULL)
    allowed_notifications_array = ArrayFieldWithChoices(choices=NotificationsTypes.choices(),
                                                        blank=True,
                                                        default=create_default_notifications,
                                                        max_length=300)
    person_info = models.ForeignKey(PersonInfo, blank=True, null=True, on_delete=models.SET_NULL)
    last_call_created_time = models.DateTimeField(blank=True, null=True)
    last_sub_project_created_time = models.DateTimeField(blank=True, null=True)
    push_notifications_status = models.CharField(max_length=30, choices=PushNotificationsStatus.choices(),
                                                 default=PushNotificationsStatus.DIDNT_ASK, blank=True)
    push_notifications_params = models.JSONField(default=dict, blank=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.donation_data = None

    def __str__(self) -> str:
        return self.get_full_name()

    def save(self, *args, **kwargs) -> None:
        super().save(*args, **kwargs)
        self.get_person_info().save()

    def get_person_info(self) -> PersonInfo:
        if self.person_info is None:
            self.person_info = PersonInfo()
            self.person_info.save()
            if self.email:
                self.person_info.set_primary_email(self.email)
            if "@" in self.username:
                self.person_info.add_email(self.username)
            self.save()
        return self.person_info

    def get_full_name(self):
        return self.get_person_info().get_full_name()

    @admin.display(description='full name')
    def full_name(self) -> str:
        return self.get_full_name()

    @admin.display(description='primary email')
    def primary_email(self) -> str:
        return self.get_primary_email()

    @admin.display(description='primary phone number')
    def primary_phone_number(self) -> str:
        return self.get_primary_phone_number()

    @classmethod
    def get_by_username(cls, username: str) -> Optional["User"]:
        try:
            return cls.objects.get(username=username)
        except cls.DoesNotExist:
            return None

    def is_admin(self) -> bool:
        return self.is_staff or self.is_superuser or Permissions.ANALYST in self.permissions_array \
            or Permissions.FINANCE_ADMIN in self.permissions_array

    def is_finance_admin(self) -> bool:
        return self.is_admin() and Permissions.FINANCE_ADMIN in self.permissions_array

    def is_template_admin(self) -> bool:
        return self.is_admin() and Permissions.EMAIL_ADMIN in self.permissions_array

    def is_email_admin(self) -> bool:
        return self.is_admin() and Permissions.EMAIL_ADMIN in self.permissions_array

    def is_client(self) -> bool:
        return self.organization is not None

    def is_expert(self) -> bool:
        return hasattr(self, "expert") and self.expert is not None and self.expert.status == ExpertStatus.ACTIVE

    def is_org_manager(self) -> bool:
        return Permissions.ORG_MANAGER in self.permissions_array

    def get_expert(self) -> Optional["Expert"]:
        return getattr(self, "expert") if self.is_expert() else None

    def get_teams(self) -> QuerySet:
        return self.organization.team_set if self.organization and self.is_org_manager() else self.teams

    def is_allowing_notification(self, notification: NotificationsTypes) -> bool:
        return notification in self.allowed_notifications_array

    def add_email(self, email: str, source: EmailSource = EmailSource.DEFAULT) -> None:
        self.get_person_info().add_email(email, source)

    def set_primary_email(self, email: str, source: EmailSource = EmailSource.DEFAULT) -> None:
        self.get_person_info().set_primary_email(email, source)

    def get_primary_email_for_sending(self) -> Optional[EmailAddress]:
        person_info = self.get_person_info()
        if person_info.is_unsubscribed:
            return None
        return person_info.get_primary_email_obj()

    def get_primary_email(self) -> Optional[str]:
        return self.get_person_info().get_primary_email()

    def get_all_emails(self) -> List[EmailAddress]:
        return self.get_person_info().get_all_emails()

    def add_phone_number(self, phone_number: str, given_by_user: bool) -> None:
        self.get_person_info().add_phone_number(phone_number, given_by_user)

    def set_primary_phone_number(self, phone_number: str, given_by_user: bool) -> None:
        self.get_person_info().set_primary_phone_number(phone_number, given_by_user)

    def get_primary_phone_number(self) -> Optional[str]:
        return self.get_person_info().get_primary_phone_number()

    def get_all_phone_numbers(self) -> List[str]:
        return self.get_person_info().get_all_phone_numbers()

    def replace_phone_number(self, old_value: str, new_value: str, given_by_user: bool) -> None:
        return self.get_person_info().replace_phone_number(old_value, new_value, given_by_user)

    def replace_primary_phone_number(self, new_value: str) -> None:
        person_info = self.get_person_info()
        old_primary_phone_number = person_info.get_primary_phone_number()
        person_info.replace_phone_number(old_primary_phone_number, new_value, True)

    @property
    def person_first_name(self) -> str:
        return self.get_person_info().first_name

    @person_first_name.setter
    def person_first_name(self, value: str) -> None:
        self.get_person_info().first_name = value

    @property
    def person_last_name(self) -> str:
        return self.get_person_info().last_name

    @person_last_name.setter
    def person_last_name(self, value: str) -> None:
        self.get_person_info().last_name = value

    @property
    def preferred_language(self) -> str:
        return self.get_person_info().preferred_language

    @preferred_language.setter
    def preferred_language(self, value: str) -> None:
        self.get_person_info().preferred_language = value

    @property
    def preferred_timezone_offset(self) -> str:
        return self.get_person_info().preferred_timezone_offset

    @preferred_timezone_offset.setter
    def preferred_timezone_offset(self, value: str) -> None:
        self.get_person_info().preferred_timezone_offset = value

    @property
    def pic_url(self) -> str:
        return self.get_person_info().pic_url

    @pic_url.setter
    def pic_url(self, value: str) -> None:
        self.get_person_info().pic_url = value

    @property
    def temporary_phone_number(self) -> str:
        return self.get_person_info().temporary_phone_number

    @temporary_phone_number.setter
    def temporary_phone_number(self, value: str) -> None:
        self.get_person_info().temporary_phone_number = value

    @property
    def is_unsubscribed(self) -> bool:
        return self.get_person_info().is_unsubscribed

    @is_unsubscribed.setter
    def is_unsubscribed(self, value: bool) -> None:
        self.get_person_info().set_is_unsubscribed(value)

    def set_is_unsubscribed(self, is_unsubscribed: bool) -> None:
        self.get_person_info().set_is_unsubscribed(is_unsubscribed)

    @classmethod
    def get_all_clients(cls) -> QuerySet:
        return cls.objects.filter(~Q(organization__isnull=True))

    @classmethod
    def get_all_expert_users(cls) -> QuerySet:
        return cls.objects.filter(~Q(expert__isnull=True))

    @classmethod
    def get_all_active_expert_users(cls) -> QuerySet:
        return cls.objects.filter(~Q(expert__isnull=True) & Q(expert__status=ExpertStatus.ACTIVE))

    @classmethod
    def email_is_available(cls, email: str) -> bool:
        return not cls.objects.filter(username=email).exists()

    @classmethod
    def email_is_available_for_new(cls, email: str) -> bool:
        return not PersonInfo.objects.filter(emails__has_key=email).exists()
