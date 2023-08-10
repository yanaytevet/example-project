from typing import Self

from django.contrib.auth.models import AbstractUser
from django.db import models

from common.db_fields.array_field_with_choices import ListFieldWithChoices
from users.consts.permissions import Permissions


class User(AbstractUser):
    list_filter = []
    raw_id_fields = []

    permissions = ListFieldWithChoices(choices=Permissions.choices(), blank=True, default=list)
    pic_url = models.CharField(max_length=255, blank=True, null=True)
    is_unsubscribed = models.BooleanField(default=False, blank=True)

    def __str__(self) -> str:
        return self.get_full_name()

    @classmethod
    async def async_get_by_username(cls, username: str) -> Self | None:
        return await cls.objects.filter(username=username).afirst()

    def is_admin(self) -> bool:
        return Permissions.ADMIN in self.permissions
