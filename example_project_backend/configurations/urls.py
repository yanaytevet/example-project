
from django.urls import path

from configurations.views.configurations_views import FullConfigurationsView

urlpatterns = [
    path(r'', FullConfigurationsView.as_view()),
]
