from django.db import models

from configurations.models.configurations import Configurations


class GUIConfigurations(Configurations):
    gui_hostname = models.CharField(max_length=200, default='', blank=True)
    backend_hostname = models.CharField(max_length=200, default='', blank=True)
    default_profile_pic = models.CharField(max_length=200, default='', blank=True)

    def get_gui_hostname(self) -> str:
        if self.gui_hostname and self.gui_hostname[-1] == '/':
            return self.gui_hostname
        return f'{self.gui_hostname}/'
