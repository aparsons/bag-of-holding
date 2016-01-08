from django.db import models
from django.contrib.humanize.templatetags.humanize import naturaltime
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse
from django.utils.functional import cached_property
from django.utils.translation import ugettext_lazy as _

from boh.core import behaviors

from . import managers, querysets


class Action(behaviors.Timestampable, models.Model):
    """Describes an actor performing a verb on an optional target."""

    actor_type = models.ForeignKey(ContentType, related_name='actor')
    actor_id = models.CharField(_('actor id'), max_length=255)
    actor = GenericForeignKey('actor_type', 'actor_id')

    verb = models.CharField(_('verb'), max_length=255)
    #description?

    action_type = models.ForeignKey(ContentType, blank=True, null=True, related_name='action')
    action_id = models.CharField(_('action id'), max_length=255, blank=True, null=True)
    action = GenericForeignKey('action_type', 'action_id')

    target_type = models.ForeignKey(ContentType, blank=True, null=True, related_name='target')
    target_id = models.CharField(_('target id'), max_length=255, blank=True, null=True)
    target = GenericForeignKey('target_type', 'target_id')

    public = models.BooleanField(_('public'), default=True)

    objects = managers.ActionManager.from_queryset(querysets.ActionQuerySet)()

    class Meta:
        ordering = ['-created']
        verbose_name = _('Action')
        verbose_name_plural = _('Actions')

    def __str__(self):
        context = {
            'actor': self.actor,
            'verb': self.verb,
            'action': self.action,
            'target': self.target,
            'timesince': self.timesince,
        }
        if self.target:
            if self.action:
                return _('%(actor)s %(verb)s %(action)s on %(target)s %(timesince)s') % context
            return _('%(actor)s %(verb)s %(target)s %(timesince)s') % context
        if self.action:
            return _('%(actor)s %(verb)s %(action)s %(timesince)s') % context
        return _('%(actor)s %(verb)s %(timesince)s') % context

    @cached_property
    def timesince(self):
        """Returns the time between created and the current time as a nicely formatted string."""
        return naturaltime(self.created)


class Follow(behaviors.Timestampable, models.Model):
    """Allows users to follow the actions of actors."""

    class Meta:
        ordering = ['-created']
        verbose_name = _('Follow')
        verbose_name_plural = _('Follows')
