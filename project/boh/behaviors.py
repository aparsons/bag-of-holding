from django.db import models


class TimeStampedModel(models.Model):
    """An abstract model allowing models to track its creation and last modified times."""

    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
