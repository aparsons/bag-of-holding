from django.contrib import admin

from . import models


class EngagementAdmin(admin.ModelAdmin):
    list_display = ['start_date', 'end_date']
admin.site.register(models.Engagement, EngagementAdmin)


admin.site.register(models.ActivityType)

<<<<<<< Updated upstream
admin.site.register(models.Worker)
=======
>>>>>>> Stashed changes

admin.site.register(models.Activity)
