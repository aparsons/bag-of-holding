from django.db import models
from django.utils.translation import ugettext_lazy as _


class Application(models.Model):
    name = models.CharField(_('name'), max_length=128, unique=True, help_text=_('The full unique name of the application.'))
    description = models.TextField(_('description'), blank=True, help_text=_('Information about the application\'s purpose, history, and design.'))

    created = models.DateTimeField(_('created'), auto_now_add=True)
    modified = models.DateTimeField(_('modified'), auto_now=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name
