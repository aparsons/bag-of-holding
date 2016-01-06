from django.db import models
from django.utils.translation import ugettext_lazy as _

from boh.core import behaviors

from . import managers, querysets


class Action(behaviors.Timestampable, models.Model):
    """Describes an actor performing a verb on an optional target."""

    objects = managers.ActionManager.from_queryset(querysets.ActionQuerySet)()

    class Meta:
        ordering = ['created']
        verbose_name = _('Action')
        verbose_name_plural = _('Actions')


class Follow(behaviors.Timestampable, models.Model):
    """Allows users to follow the actions of actors."""

    class Meta:
        ordering = ['created']
        verbose_name = _('Follow')
