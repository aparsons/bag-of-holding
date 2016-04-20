from datetime import timedelta

from django.core.validators import RegexValidator
from django.db import models
from django.utils import timezone
from django.utils.functional import cached_property
from django.utils.translation import ugettext_lazy as _

from boh.core import behaviors
from boh.core.organizations import models as organizations_models

from . import managers, querysets


class Environment(behaviors.Timestampable, models.Model):
    """Information about an application deployment environment."""

    description = models.TextField(_('description'), blank=True, help_text=_('Information about the environment\'s purpose, physical location, hardware, and deployment.'))
    testing_approved = models.BooleanField(_('testing approved'), default=False, help_text=_('Specify if security testing has been approved for this environment.'))


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


class Tag(behaviors.Timestampable, models.Model):
    """Abstract label applied to applications for search and categorization."""

    color_regex = RegexValidator(regex=r'^[0-9A-Fa-f]{6}$', message=_('Color must be entered in the 6 character hex format.'))

    name = models.CharField(_('name'), max_length=64, unique=True, help_text=_('A unique name for this tag.'))
    color = models.CharField(_('color'), max_length=6, validators=[color_regex], help_text=_('Specify a 6 character hexadecimal color value. (e.g., \'d94d59\')'))
    tooltip = models.CharField(_('tooltip'), max_length=64, blank=True, help_text=_('A short description of this tag\'s purpose to be shown in tooltips.'))

    class Meta:
        ordering = ['name']
        verbose_name = _('Tag')
        verbose_name_plural = _('Tags')

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
    environments = models.ManyToManyField(Environment, blank=True, verbose_name=_('Environments'))
    regulations = models.ManyToManyField(Regulation, blank=True, verbose_name=_('Regulations'))
    tags = models.ManyToManyField(Tag, blank=True, verbose_name=_('Tags'))
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
