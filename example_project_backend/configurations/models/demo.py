
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from common.django_utils.model_utils import ModelUtils


class Demo(models.Model):
    key = models.CharField(max_length=255, default=str, blank=True)
    data = models.JSONField(default=None, blank=True)
    name_hash = models.CharField(max_length=255, default=None, blank=True)


@receiver(post_save, sender=Demo)
def data_changed(sender, instance, created, **kwargs):
    name_hash = ModelUtils.get_hash_by_fields(instance, ['key', 'data'])
    if name_hash != instance.name_hash:
        instance.name_hash = name_hash
        instance.save()
