from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.core import validators
from django.db import models
from django.utils.translation import ugettext_lazy as _

from boh.core import behaviors

from . import managers, querysets


class User(behaviors.Timestampable, AbstractBaseUser, PermissionsMixin):
    username = models.CharField(
        _('username'),
        max_length=254,
        unique=True,
        help_text=_('Required. 254 characters or fewer. Letters, digits and @/./+/-/_ only.'),
        validators=[
            validators.RegexValidator(r'^[\w.@+-]+$', _('Enter a valid username. This value may contain only letters, numbers, and @/./+/-/_ characters.'))
        ],
        error_messages={
            'unique': _("A user with that username already exists."),
        },
    )
    first_name = models.CharField(_('first name'), max_length=30, help_text=_(''))
    last_name = models.CharField(_('last name'), max_length=30, help_text=_(''))
    email = models.EmailField(_('email address'), help_text=_(''))
    is_active = models.BooleanField(_('active'), default=True, help_text=_('Designates whether this user should be treated as active. Unselect this instead of deleting accounts.'))
    is_staff = models.BooleanField(_('staff'), default=False, help_text=_('Designates whether the user can log into this admin site.'))

    objects = managers.UserManager.from_queryset(querysets.UserQuerySet)()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'email']

    class Meta:
        ordering = ['username']
        verbose_name = _('User')
        verbose_name_plural = _('Users')

    def __str__(self):
        return self.get_full_name()

    def get_full_name(self):
        """Returns the first name and last name."""
        return '%s %s' % (self.first_name, self.last_name)

    def get_short_name(self):
        """Returns the first name for the user."""
        return self.first_name
