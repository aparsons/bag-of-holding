from django.db import models
from django.utils.translation import ugettext_lazy as _

from boh.core import behaviors
from boh.core.applications import models as applications_models


class Engagement(behaviors.Timestampable, models.Model):
    """A collection of activities to be performed."""

    start_date = models.DateField(_('start date'), help_text=_('The date the engagement is scheduled to begin.'))
    end_date = models.DateField(_('end date'), help_text=_('The date the engagement is scheduled to conclude.'))
    description = models.TextField(_('description'), blank=True, help_text=_('Optional information about the engagement\'s objectives, scope, and methodology.'))

    applications = models.ManyToManyField(applications_models.Application, blank=True, verbose_name=_('Application'), help_text=_('The applications included in the engagement.'))

    class Meta:
        ordering = ['start_date']
        verbose_name = _('Engagement')
        verbose_name_plural = _('Engagements')


class ActivityType(behaviors.Timestampable, models.Model):
    """The type of work to be performed during an activity."""

    name = models.CharField(_('name'), max_length=128, unique=True, help_text=_('A unique name for this activity type.'))

    class Meta:
        ordering = ['name']
        verbose_name = _('Activity Type')
        verbose_name_plural = _('Activity Types')

    def __str__(self):
        return self.name


class Activity(behaviors.Timestampable, models.Model):
    """A unit of work performed over the course of an engagement."""

    description = models.TextField(_('description'), blank=True, help_text=_('Optional information about the activity.'))

    activity_type = models.ForeignKey(ActivityType, verbose_name=_('Activity Type'), help_text=_('The type of activity to be performed.'))
    engagement = models.ForeignKey(Engagement, verbose_name=_('Engagement'), help_text=_('The engagement containing the activity.'))

    class Meta:
        verbose_name = _('Activity')
        verbose_name_plural = _('Activities')
