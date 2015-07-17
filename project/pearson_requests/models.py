from django.db import models

from boh.models import ActivityType


class ServiceBundle(models.Model):
    """A collection of activities able to be publicly requested."""
    name = models.CharField(max_length=128)
    description = models.CharField(max_length=255)
    time_estimate = models.CharField(max_length=64)
    activities = models.ManyToManyField(ActivityType)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

"""
- Requestor Info
- Application
- Application Description

- Metadata
  - Platform
  - Lifecycle (Optional)
  - Origin
  - Criticality

- Technologies (Optional)
- Regulations (Optional)

- Activities
- Availablity Date Window
- Project deadline?

- Status: Recieved, Waiting for Response, Declined, Approved (Readonly),

- Remarks

- Software Version? (Optional)

Manual Assessment

AppScan Setup

Checkmarx
 - Source Code Repository

Veracode
"""
