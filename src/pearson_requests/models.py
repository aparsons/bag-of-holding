from django.db import models
from django.utils.translation import ugettext as _

from boh.models import ActivityType


class DefaultSubscriber(models.Model):
    name = models.CharField(max_length=128, help_text=_('Name of the person or group subscribed to the engagement request.'))
    email = models.EmailField(help_text=_('The email address that will be receiving notifications.'))
    label = models.CharField(max_length=16, blank=True, help_text=_('An optional brief description about this subscription.'))

    send_status_updates = models.BooleanField(default=True, help_text=_('Notify the subscriber when the engagement request status changes.'))
    send_comments = models.BooleanField(default=True, help_text=_('Notify the subscriber when new comments are submitted.'))

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class ServiceBundle(models.Model):
    """A collection of activities able to be publicly requested."""

    name = models.CharField(max_length=35)
    brief_description = models.CharField(max_length=60)
    detailed_description = models.TextField(blank=True, help_text=_('A detailed description shown when "More Information" is clicked. Markdown can be used.'))
    time_estimate = models.CharField(max_length=64)

    show_appscan_form = models.BooleanField(default=False, help_text=_('Specify if AppScan information should be requested.'))
    show_checkmarx_form = models.BooleanField(default=False, help_text=_('Specify if information needed to setup Checkmarx is requested.'))

    activities = models.ManyToManyField(ActivityType, related_name='activites')
    default_subscribers = models.ManyToManyField(DefaultSubscriber, blank=True, help_text=_('These subscribers will automatically be added to work requests for this service bundle.'))

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

