from django.db import models
from django.utils.translation import ugettext_lazy as _

from boh.core import behaviors


class Organization(behaviors.Timestampable, models.Model):
    """A top-level entity to represent a business or group of people."""

    name = models.CharField(_('name'), max_length=128, unique=True, help_text=_('The full unique name of the organization.'))
    description = models.TextField(_('description'), blank=True, help_text=_('Information about the application\'s purpose, history, and structure.'))

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name
