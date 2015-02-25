from django.conf.urls import patterns, include, url

from tracker import views

urlpatterns = patterns('',

	# Application Routes
    url(r'^applications/$', views.application_list, name='application.list'),
    url(r'^applications/add/$', views.application_add, name='application.add'),
    url(r'^applications/(?P<application_id>\d+)/$', views.application_detail, name='application.detail'),
    url(r'^applications/(?P<application_id>\d+)/edit/$', views.application_edit, name='application.edit'),
    url(r'^applications/(?P<application_id>\d+)/delete/$', views.application_delete, name='application.delete'),

    # Engagement Routes
    url(r'^applications/(?P<application_id>\d+)/engagements/add/$', views.engagement_add, name='engagement.add'),
    url(r'^engagements/(?P<engagement_id>\d+)/$', views.engagement_detail, name='engagement.detail'),
    url(r'^engagements/(?P<engagement_id>\d+)/edit/$', views.engagement_edit, name='engagement.edit'),
    url(r'^engagements/(?P<engagement_id>\d+)/delete/$', views.engagement_delete, name='engagement.delete'),
    url(r'^engagements/(?P<engagement_id>\d+)/comments/add/$', views.engagement_comment_add, name='engagement.comment.add'),

    # Activity Routes
    url(r'^engagements/(?P<engagement_id>\d+)/activities/add/$', views.activity_add, name='activity.add'),
    url(r'^activities/(?P<activity_id>\d+)/$', views.activity_detail, name='activity.detail'),
    url(r'^activities/(?P<activity_id>\d+)/edit/$', views.activity_edit, name='activity.edit'),
    url(r'^activities/(?P<activity_id>\d+)/delete/$', views.activity_delete, name='activity.delete'),
    url(r'^activities/(?P<activity_id>\d+)/comments/add/$', views.activity_comment_add, name='activity.comment.add'),

    # People Routes
    url(r'^people/$', views.people_list, name='people.list'),

)
