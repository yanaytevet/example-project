from django.db import models

from common.django_utils.model_utils import ModelUtils
from common.type_hints import JSONType


class Configurations(models.Model):
    list_filter = []

    class Meta:
        abstract = True

    @classmethod
    def get(cls) -> 'Configurations':
        obj, _ = cls.objects.get_or_create({})
        return obj

    @classmethod
    def get_as_json(cls) -> JSONType:
        return ModelUtils.to_json(cls.get())
