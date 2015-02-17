from django.conf.urls import patterns, include, url
from django.contrib.auth.decorators import login_required

from tracker import views

urlpatterns = patterns('',

	# Application Routes
    url(r'^applications/$', views.application_list, name='application.list'),
    url(r'^applications/(?P<application_id>\d+)/$', views.application_detail, name='application.detail'),
    url(r'^applications/add/$', views.application_add, name='application.add'),
    url(r'^applications/(?P<application_id>\d+)/edit/$', views.application_edit, name='application.edit'),
    url(r'^applications/(?P<application_id>\d+)/delete/$', views.application_delete, name='application.delete'),

    # Engagement Routes
    url(r'^applications/(?P<application_id>\d+)/engagements/add/$', views.engagement_add, name='engagement.add'),
    url(r'^engagements/(?P<engagement_id>\d+)/$', views.engagement_detail, name='engagement.detail'),
    url(r'^engagements/(?P<engagement_id>\d+)/comments/add/$', views.engagement_comment_add, name='engagement.comment.add'),

    # Activity Routes
    url(r'^engagements/(?P<engagement_id>\d+)/activities/add/$', views.activity_add, name='activity.add'),
    url(r'^activities/(?P<activity_id>\d+)/$', views.activity_detail, name='activity.detail'),

)
