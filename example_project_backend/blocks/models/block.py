from django.db import models

from blocks.consts.block_types import BlockTypes


class Block(models.Model):
    list_filter = []

    a = models.TextField(default='', blank=True)
    b = models.IntegerField(default=0, blank=True)
    c = models.BooleanField(default=False, blank=True)
    block_type = models.CharField(max_length=255, choices=BlockTypes.choices(), blank=True, default=BlockTypes.ROUND)
