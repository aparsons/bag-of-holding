from django.db import models
from datetime import timedelta
from django.utils import timezone


class TimeStampedModel(models.Model):
    """An abstract model allowing models to track its creation and last modified times."""

    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

    def is_new(self):
        """Returns true if the application was created in the last 7 days"""
        delta = self.created_date - timezone.now()
        return delta >= timedelta(days=-7)
