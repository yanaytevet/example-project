from django.db import models


class ExampleModel(models.Model):
    list_filter = []

    a = models.TextField(default='', blank=True)
    b = models.IntegerField(default=0, blank=True)
    c = models.BooleanField(default=False, blank=True)
