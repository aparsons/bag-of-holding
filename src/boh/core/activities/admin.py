from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from . import models


class EventAdmin(admin.ModelAdmin):
    date_hierarchy = 'created'
    fieldsets = (
        (_('Actor'), {
            'fields': (('actor_type', 'actor_id'),)
        }),
        (_('Verb'), {
            'fields': ('verb',)
        }),
        (_('Action'), {
            'fields': (('action_type', 'action_id'),)
        }),
        (_('Preposition'), {
            'fields': ('preposition',)
        }),
        (_('Target'), {
            'fields': (('target_type', 'target_id'),)
        }),
        (_('Metadata'), {
            'fields': ('public', 'created', 'modified')
        }),
    )
    list_display = ['__str__', 'actor', 'verb', 'action', 'preposition', 'target', 'public', 'created']
    list_filter = ['public', 'created']
    readonly_fields = ['created', 'modified']
    search_fields = ['verb']
admin.site.register(models.Event, EventAdmin)


class FollowAdmin(admin.ModelAdmin):
    date_hierarchy = 'created'
    fieldsets = (
        (_('User'), {
            'fields': ('user',)
        }),
        (_('Actor'), {
            'fields': (('actor_type', 'actor_id'),)
        }),
        (_('Metadata'), {
            'fields': ('created', 'modified')
        }),
    )
    list_display = ['__str__', 'user', 'actor', 'created']
    list_filter = ['created']
    readonly_fields = ['created', 'modified']
admin.site.register(models.Follow, FollowAdmin)
