from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserChangeForm

from common.admin_utils.register_models_to_admin import ModelRegisterer
from users import models
from users.models import User

ModelRegisterer(models, ignore_models=[User]).register()


class CustomUserAdmin(UserAdmin):
    form = UserChangeForm
    list_display = (
        'id',
        'username',
        'email',
    )
    list_filter = []
    raw_id_fields = []
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('email',)}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
        (
            'Custom Field Heading',
            {
                'fields': (
                    'permissions',
                ),
            },
        ),
    )


admin.site.register(User, CustomUserAdmin)


