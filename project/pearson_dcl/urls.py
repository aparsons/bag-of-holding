from django.conf.urls import patterns, include, url

from . import views


urlpatterns = [
    url(r'^$', views.index, name='index'),
]
