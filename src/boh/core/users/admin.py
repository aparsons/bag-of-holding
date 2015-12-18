from django.contrib import admin
from django.contrib.auth import admin as auth_admin
from django.utils.translation import ugettext_lazy as _

from . import models


class UserAdmin(auth_admin.UserAdmin):
    add_fieldsets = (
        (_('Credentials'), {
           'fields': ('username', 'password1', 'password2')
        }),
        (_('Profile'), {
            'fields': ('first_name', 'last_name', 'email')
        }),
    )
    fieldsets = (
        (_('Credentials'), {
            'fields': ('username', 'password')
        }),
        (_('Profile'), {
            'fields': ('first_name', 'last_name', 'email')
        }),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser')
        }),
        (_('Miscellaneous'), {
            'fields': ('last_login', 'created', 'modified')
        })
    )
    list_display = ['username', 'first_name', 'last_name', 'email', 'last_login', 'is_active', 'is_staff', 'is_superuser']
    readonly_fields = ['created', 'modified', 'last_login']
    search_fields = ['username', 'first_name', 'last_name', 'email']
admin.site.register(models.User, UserAdmin)
