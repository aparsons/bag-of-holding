from django.db import models
from django.utils.translation import ugettext_lazy as _

from boh.core import behaviors
from boh.core.organizations import models as organizations_models


class Application(behaviors.Timestampable, models.Model):
    name = models.CharField(_('name'), max_length=128, unique=True, help_text=_('The full unique name of the application.'))
    description = models.TextField(_('description'), blank=True, help_text=_('Information about the application\'s purpose, history, and design.'))

    organization = models.ForeignKey(organizations_models.Organization, blank=True, null=True, help_text=_('The organization under which the application belongs.'))

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name
