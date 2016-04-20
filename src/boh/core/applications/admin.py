from django.contrib import admin

from . import models


admin.site.register(models.Environment)


admin.site.register(models.Regulation)


admin.site.register(models.Tag)


admin.site.register(models.Technology)


class ApplicationAdmin(admin.ModelAdmin):
    date_hierarchy = 'created'
    list_display = ['name', 'organization']
    list_filter = ['created']
    readonly_fields = ['created', 'modified']
    search_fields = ['name']
admin.site.register(models.Application, ApplicationAdmin)
