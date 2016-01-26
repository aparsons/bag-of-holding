from django.db import models
from django.utils.translation import ugettext_lazy as _


class Observable(models.Model):
    """An abstract base class model that provides a method to obtain a feed of events involving the model instance."""

    def activity_feed(self):
        """Returns all public events for the model instance."""
        from boh.core.activities.models import Event
        return Event.objects.any(self)

    class Meta:
        abstract = True


class Timestampable(models.Model):
    """An abstract base class model that provides self-updating 'created' and 'modified' fields."""

    created = models.DateTimeField(_('created'), auto_now_add=True)
    modified = models.DateTimeField(_('modified'), auto_now=True)

    class Meta:
        abstract = True


