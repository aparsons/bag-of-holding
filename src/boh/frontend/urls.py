"""
URL Configuration
https://docs.djangoproject.com/en/1.9/topics/http/urls/
"""

from django.conf.urls import url

from .views import home as home_views
from .views import applications as applications_views
from .views import engagements as engagements_views

urlpatterns = [

    # Home
    url(r'^$', home_views.index, name='home'),

    # Applications
    url(r'^applications/$', applications_views.list, name='applications.list'),
    url(r'^applications/(?P<application_id>\d+)/$', applications_views.overview, name='applications.overview'),
        # Engagements
    url(r'^applications/(?P<application_id>\d+)/benchmarks/$', applications_views.benchmarks, name='applications.benchmarks'),
        # Environments
        # Documentation
        # Settings

    # Engagements
    url(r'^engagements/$', engagements_views.list, name='engagements.list'),

]
