from django.db import models

from configurations.enums.storages_types import StoragesTypes
from configurations.models.configurations import Configurations


class StorageConfigurations(Configurations):
    list_filter = []

    storage_type = models.CharField(max_length=100, default=StoragesTypes.NONE, blank=True,
                                    choices=StoragesTypes.choices())
    storage_params = models.JSONField(default=dict, blank=True)

    dev_storage_type = models.CharField(max_length=100, default=StoragesTypes.NONE, blank=True,
                                        choices=StoragesTypes.choices())
    dev_storage_params = models.JSONField(default=dict, blank=True)
