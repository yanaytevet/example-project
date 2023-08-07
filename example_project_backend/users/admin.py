from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserChangeForm
from django.db.models import Q

from common.django_utils.admin_utils import register_all_classes
from users import models
from .consts.time_zones import get_time_zones_tup
from .models import User

register_all_classes(models, ignore_models=[User])


class CustomUserChangeForm(UserChangeForm):
    person_first_name = forms.CharField(label="First Name")
    person_last_name = forms.CharField(label="Last Name")
    primary_email = forms.CharField(label="Primary Email")
    primary_phone_number = forms.CharField(label="Primary Phone Number", required=False)
    time_zone = forms.ChoiceField(label="Time Zone", choices=get_time_zones_tup())

    class Meta:
        exclude = []
        model = User

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        first_name_field = self.fields.get('person_first_name')
        first_name_field.initial = self.instance.person_first_name

        last_name_field = self.fields.get('person_last_name')
        last_name_field.initial = self.instance.person_last_name

        primary_email_field = self.fields.get('primary_email')

        email_obj = self.instance.get_primary_email_for_sending()
        primary_email_field.initial = email_obj.address if email_obj else None

        primary_phone_number_field = self.fields.get('primary_phone_number')
        primary_phone_number_field.initial = self.instance.get_primary_phone_number()

        time_zone_field = self.fields.get('time_zone')
        time_zone_field.initial = self.instance.preferred_timezone_offset

    def save(self, commit=True):
        self.instance.person_first_name = self.cleaned_data['person_first_name']
        self.instance.person_last_name = self.cleaned_data['person_last_name']
        self.instance.set_primary_email(self.cleaned_data['primary_email'])
        self.instance.replace_primary_phone_number(self.cleaned_data['primary_phone_number'])
        self.instance.preferred_timezone_offset = self.cleaned_data['time_zone']
        return super().save(commit=commit)


class IsExpertListFilter(admin.SimpleListFilter):
    title = 'Is Expert'
    parameter_name = 'is_expert'

    def lookups(self, request, model_admin):
        return (
            ('True', 'True'),
            ('False', 'False'),
        )

    def queryset(self, request, queryset):
        if self.value() == 'True':
            return queryset.filter(expert__isnull=False)
        elif self.value() == 'False':
            return queryset.filter(expert__isnull=True)
        return queryset


class CustomUserAdmin(UserAdmin):
    form = CustomUserChangeForm
    list_display = (
        'id',
        'username',
        'primary_email',
        'primary_phone_number',
        'full_name',
        'is_staff',
        'is_expert',
    )
    list_filter = (
        IsExpertListFilter,
    )
    raw_id_fields = ['person_info', 'teams']
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('person_first_name', 'person_last_name', 'primary_email', 'primary_phone_number',
                                      'time_zone')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
        (
            'Custom Field Heading',
            {
                'fields': (
                    'person_info',
                    'permissions_array',
                    'organization',
                    'teams',
                    'allowed_notifications_array',
                    'last_call_created_time',
                    'last_sub_project_created_time',
                    'push_notifications_status',
                    'push_notifications_params',
                ),
            },
        ),
    )


admin.site.register(User, CustomUserAdmin)
