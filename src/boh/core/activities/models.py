from django.conf import settings
from django.contrib.humanize.templatetags.humanize import naturaltime
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils.functional import cached_property
from django.utils.translation import ugettext_lazy as _

from boh.core import behaviors

from . import managers, querysets


class Event(behaviors.Timestampable, models.Model):
    """Describes an actor performing a verb on an optional target."""

    actor_type = models.ForeignKey(ContentType, related_name='actor')
    actor_id = models.CharField(_('actor id'), max_length=255)
    actor = GenericForeignKey('actor_type', 'actor_id')

    verb = models.CharField(_('verb'), max_length=255)

    action_type = models.ForeignKey(ContentType, blank=True, null=True, related_name='action')
    action_id = models.CharField(_('action id'), max_length=255, blank=True, null=True)
    action = GenericForeignKey('action_type', 'action_id')

    preposition = models.CharField(_('preposition'), max_length=255, blank=True, null=True)

    target_type = models.ForeignKey(ContentType, blank=True, null=True, related_name='target')
    target_id = models.CharField(_('target id'), max_length=255, blank=True, null=True)
    target = GenericForeignKey('target_type', 'target_id')

    public = models.BooleanField(_('public'), default=True)

    objects = managers.EventManager.from_queryset(querysets.EventQuerySet)()

    class Meta:
        ordering = ['-created']
        verbose_name = _('Event')
        verbose_name_plural = _('Events')

    def __str__(self):
        context = {
            'actor': self.actor,
            'verb': self.verb,
            'action': self.action,
            'preposition': self.preposition,
            'target': self.target,
            'timesince': self.timesince,
        }
        if self.target:
            if self.action:
                return _('%(actor)s %(verb)s %(action)s %(preposition)s %(target)s %(timesince)s') % context
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

    user = models.ForeignKey(settings.AUTH_USER_MODEL)

    actor_type = models.ForeignKey(ContentType)
    actor_id = models.CharField(_('actor id'), max_length=255)
    actor = GenericForeignKey('actor_type', 'actor_id')

    objects = managers.FollowManager.from_queryset(querysets.FollowQuerySet)()

    class Meta:
        ordering = ['-created']
        unique_together = ('user', 'actor_type', 'actor_id')
        verbose_name = _('Follow')
        verbose_name_plural = _('Follows')

    def __str__(self):
        return '%s -> %s' % (self.user, self.actor)
