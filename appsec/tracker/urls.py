from django.conf.urls import patterns, include, url
from django.contrib.auth.decorators import login_required

from tracker import views

urlpatterns = patterns('',

    url(r'^applications/$', views.application_list, name='applications.list'),
    url(r'^applications/(?P<application_id>\d+)/$', views.application_detail, name='application.detail'),
    url(r'^applications/add/$', views.application_add, name='application.add'),
    url(r'^applications/(?P<application_id>\d+)/edit/$', views.application_edit, name='application.edit'),
    url(r'^applications/(?P<application_id>\d+)/delete/$', views.application_delete, name='application.delete'),

    url(r'^applications/(?P<application_id>\d+)/engagements/add/$', views.engagement_add, name='engagement.add'),
    url(r'^engagements/(?P<engagement_id>\d+)/$', views.engagement_detail, name='engagement.detail'),

)
