from django.contrib import admin

from . import models


class ServiceBundleAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'time_estimate', 'activities_list']
    search_fields = ['^name']

    def activities_list(self, obj):
        return ', '.join([str(a) for a in obj.activities.all()])
    activities_list.short_description = 'Activities'

admin.site.register(models.ServiceBundle, ServiceBundleAdmin)
