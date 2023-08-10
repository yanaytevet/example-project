from django.db import models

from configurations.models.configurations import Configurations


class UsersEventsConfigurations(Configurations):
    list_display = ['id', 'should_analyze_events']

    should_analyze_events = models.BooleanField(default=False, blank=True)
    events_analysis_params = models.JSONField(default=dict, blank=True)
