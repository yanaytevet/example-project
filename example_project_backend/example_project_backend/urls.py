
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path(r'admin/', admin.site.urls),
    path(r'admin/log_viewer/', include('log_viewer.urls')),

    path(r'auth/', include('users.auth_urls')),
    path(r'register/', include('users.registrations_urls')),
    path(r'api/users/', include('users.users_urls')),
    path(r'api/user-events/', include('users.user_events_urls')),

    path(r'api/configurations/', include('configurations.urls')),
]
