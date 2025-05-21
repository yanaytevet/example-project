from django.contrib import admin
from django.urls import path, include

from users.auth_router import api as auth_api
from users.users_router import api as users_api
from configurations.configurations_router import api as configurations_api
from blocks.blocks_router import api as blocks_api


urlpatterns = [
    path(r'admin/', admin.site.urls),
    path(r'admin/log_viewer/', include('log_viewer.urls')),

    path(r'auth/', auth_api.urls),
    path(r'users/', users_api.urls),
    path(r'configurations/', configurations_api.urls),
    path(r'blocks/', blocks_api.urls),
]
