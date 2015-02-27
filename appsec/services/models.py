from django.db import models

# Create your models here.

class ThreadFix(models.Model):
    host = models.URLField()
    port = models.PositiveIntegerField(default=8080)

    class Meta:
        verbose_name = "ThreadFix"
        verbose_name_plural = 'ThreadFix'
