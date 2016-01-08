from django.contrib import admin

from . import models


class ActionAdmin(admin.ModelAdmin):
    date_hierarchy = 'created'
    list_display = ['__str__', 'actor', 'verb', 'action', 'target', 'public', 'created']
    list_filter = ['public', 'created']
    readonly_fields = ['created', 'modified']
admin.site.register(models.Action, ActionAdmin)


admin.site.register(models.Follow)
