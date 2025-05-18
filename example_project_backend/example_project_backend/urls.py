from django.contrib import admin
from django.urls import path, include
from ninja import NinjaAPI, Router
from ninja.errors import ValidationError

from common.simple_api.exception_handler import custom_exception_handler
from configurations.configurations_router import router as configurations_router
from users.auth_router import router as auth_router
from users.users_router import router as users_router
from blocks.blocks_router import router as blocks_router

full_api = NinjaAPI()
full_api.exception_handler(ValidationError)(custom_exception_handler)
full_api.add_router('/auth/', auth_router)

api_router = Router()
full_api.add_router('/api/', api_router)

api_router.add_router('configurations/', configurations_router)
api_router.add_router('users/', users_router)
api_router.add_router('blocks/', blocks_router)


urlpatterns = [
    path(r'admin/', admin.site.urls),
    path(r'admin/log_viewer/', include('log_viewer.urls')),
    path(r'', full_api.urls),
]
