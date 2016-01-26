from django.db import models

from boh.core.activities.models import Event


class ApplicationManager(models.Manager):
    def create_application(self, name):
        return self.create(name=name)

    def activity_feed(self, application):
        """Returns public events performed on the specified application."""
        return Event.objects.target(application).public()

