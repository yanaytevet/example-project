from ninja import Router

from configurations.views.configurations_views import FullConfigurationsView

router = Router()

FullConfigurationsView.register_get(router, '')
