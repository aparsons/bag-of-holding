from django.contrib import admin

from . import models


admin.site.register(models.Technology)


class ApplicationAdmin(admin.ModelAdmin):
    list_display = ['name', 'organization']
    readonly_fields = ['created', 'modified']
    search_fields = ['name']
admin.site.register(models.Application, ApplicationAdmin)
