from django.db import models
from django.utils.translation import ugettext_lazy as _


class Timestampable(models.Model):
    """An abstract base class model that provides self-updating 'created' and 'modified' fields."""

    created = models.DateTimeField(_('created'), auto_now_add=True)
    modified = models.DateTimeField(_('modified'), auto_now=True)

    class Meta:
        abstract = True
