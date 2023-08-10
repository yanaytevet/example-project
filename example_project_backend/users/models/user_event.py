from typing import Self

from django.db import models
from django.db.models import JSONField

from common.time_utils import TimeUtils
from users.models import User


class UserEvent(models.Model):
    search_fields = ['id', 'name', 'user__first_name', 'user__last_name', 'attributes']
    list_filter = ['name']
    raw_id_fields = ['user']

    name = models.CharField(max_length=320)
    tab_id = models.CharField(max_length=120, default='', null=True, blank=True)
    attributes = JSONField(default=dict, null=True, blank=True)
    creation_time = models.DateTimeField(default=TimeUtils.now)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, db_index=True)

    @classmethod
    def get_latest_by_user(cls, user: User) -> Self | None:
        manager = cls.objects.filter(user_id=user.id).order_by('-creation_time')
        if manager.count():
            return manager.first()
        return None
