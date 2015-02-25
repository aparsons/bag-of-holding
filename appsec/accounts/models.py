from django.conf import settings
from django.db import models

# Create your models here.

class UserProfile(models.Model):
    """Contains per-user configurations."""
    name = models.CharField(max_length=128, unique=True)
    user = models.OneToOneField(settings.AUTH_USER_MODEL)
