from django.contrib import admin

from . import models


admin.site.register(models.Engagement)

admin.site.register(models.ActivityType)

admin.site.register(models.Activity)
