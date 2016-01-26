from datetime import timedelta

from django.db import models
from django.utils import timezone
from django.utils.functional import cached_property
from django.utils.translation import ugettext_lazy as _

from boh.core import behaviors
from boh.core.organizations import models as organizations_models

from . import managers, querysets


class Regulation(behaviors.Timestampable, models.Model):
    """Legislation applicable to an application."""

    name = models.CharField(_('name'), max_length=128, help_text=_('The name of the legislation.'))
    acronym = models.CharField(_('acronym'), max_length=20, unique=True, help_text=_('A shortened representation of the name.'))

    class Meta:
        ordering = ['name']
        verbose_name = _('Regulation')
        verbose_name_plural = _('Regulations')

    def __str__(self):
        return self.name


class Technology(behaviors.Timestampable, models.Model):
    """Architectural elements of an application."""

    name = models.CharField(_('name'), max_length=64, help_text='The name of the technology.')

    class Meta:
        ordering = ['name']
        verbose_name = _('Technology')
        verbose_name_plural = _('Technologies')

    def __str__(self):
        return self.name


class Application(behaviors.Observable, behaviors.Timestampable, models.Model):
    """A program or piece of software."""

    name = models.CharField(_('name'), max_length=128, unique=True, help_text=_('The full unique name of the application.'))
    description = models.TextField(_('description'), blank=True, help_text=_('Information about the application\'s purpose, history, and design.'))

    organization = models.ForeignKey(organizations_models.Organization, blank=True, null=True, verbose_name=_('Organization'), help_text=_('The organization under which the application belongs.'))
    regulations = models.ManyToManyField(Regulation, blank=True, verbose_name=_('Regulations'))
    technologies = models.ManyToManyField(Technology, blank=True, verbose_name=_('Technologies'))

    objects = managers.ApplicationManager.from_queryset(querysets.ApplicationQuerySet)()

    class Meta:
        ordering = ['name']
        verbose_name = _('Application')
        verbose_name_plural = _('Applications')

    def __str__(self):
        return self.name

    @cached_property
    def is_new(self):
        """Returns true if the application was created within the last 7 days."""
        delta = self.created - timezone.now()
        return delta >= timedelta(days=-7)
