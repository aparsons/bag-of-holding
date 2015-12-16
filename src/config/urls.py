"""
URL Configuration
https://docs.djangoproject.com/en/1.9/topics/http/urls/
"""

from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^', include('boh.frontend.urls', namespace='frontend')),
    url(r'^admin/', admin.site.urls),
]
