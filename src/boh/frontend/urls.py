"""
URL Configuration
https://docs.djangoproject.com/en/1.9/topics/http/urls/
"""

from django.conf.urls import url

from .views import applications as applications_views

urlpatterns = [

    # Applications
    url(r'^applications/$', applications_views.list, name='applications.list')

]
