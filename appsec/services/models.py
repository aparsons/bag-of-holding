from django.db import models

# Create your models here.

class ThreadFix(models.Model):
    host = models.URLField()
    port = models.PositiveIntegerField(default=8080)
    api_key = models.CharField(max_length=50)
    # 7dx5LHFksAChi0QL6XuoNIPqDjKBn2IxmW4mtqLFg
    # https://github.com/denimgroup/threadfix/blob/dev/threadfix-main/src/main/java/com/denimgroup/threadfix/service/APIKeyServiceImpl.java#L103

    class Meta:
        verbose_name = "ThreadFix"
        verbose_name_plural = 'ThreadFix'
