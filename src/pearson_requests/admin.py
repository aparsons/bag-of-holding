from django.contrib import admin

from . import models


class DefaultSubscriberAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'label', 'send_status_updates', 'send_comments']
admin.site.register(models.DefaultSubscriber, DefaultSubscriberAdmin)


class ServiceBundleAdmin(admin.ModelAdmin):
    list_display = ['name', 'brief_description', 'time_estimate', 'activities_list', 'show_appscan_form', 'show_checkmarx_form']
    search_fields = ['^name']

    def activities_list(self, obj):
        return ', '.join([str(a) for a in obj.activities.all()])
    activities_list.short_description = 'Activities'

admin.site.register(models.ServiceBundle, ServiceBundleAdmin)
