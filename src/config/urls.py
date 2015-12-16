"""
URL Configuration
https://docs.djangoproject.com/en/1.9/topics/http/urls/
"""

from django.conf.urls import url
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', admin.site.urls),
]
