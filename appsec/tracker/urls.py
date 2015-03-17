from django.conf.urls import patterns, include, url

from tracker import views

urlpatterns = patterns('',

    # Dashboard
    url(r'^$', views.dashboard_personal, name='dashboard.personal'),
    url(r'^team/$', views.dashboard_team, name='dashboard.team'),
    url(r'^metrics/$', views.dashboard_metrics, name='dashboard.metrics'),
    url(r'^reports/$', views.dashboard_reports, name='dashboard.reports'),

    # Management
    url(r'^manage/services/$', views.management_services, name='management.services'),
    url(r'^manage/users/$', views.management_users, name='management.users'),

    # Organization
    url(r'^organizations/add/$', views.organization_add, name='organization.add'),
    url(r'^organizations/(?P<organization_id>\d+)/$', views.organization_overview, name='organization.overview'),
    url(r'^organizations/(?P<organization_id>\d+)/people/$', views.organization_people, name='organization.people'),
    url(r'^organizations/(?P<organization_id>\d+)/settings/$', views.organization_settings_general, name='organization.settings.general'),
    url(r'^organizations/(?P<organization_id>\d+)/settings/danger/$', views.organization_settings_danger, name='organization.settings.danger'),

	# Application
    url(r'^applications/$', views.application_list, name='application.list'),
    url(r'^applications/add/$', views.application_add, name='application.add'),
    url(r'^applications/(?P<application_id>\d+)/$', views.application_overview, name='application.overview'),
    url(r'^applications/(?P<application_id>\d+)/engagements/$', views.application_engagements, name='application.engagements'),
    url(r'^applications/(?P<application_id>\d+)/environments/$', views.application_environments, name='application.environments'),
    url(r'^applications/(?P<application_id>\d+)/people/$', views.application_people, name='application.people'),
    url(r'^applications/(?P<application_id>\d+)/settings/$', views.application_settings_general, name='application.settings.general'),
    url(r'^applications/(?P<application_id>\d+)/settings/metadata/$', views.application_settings_metadata, name='application.settings.metadata'),
    url(r'^applications/(?P<application_id>\d+)/settings/data-elements/$', views.application_settings_data_elements, name='application.settings.data-elements'),
    url(r'^applications/(?P<application_id>\d+)/settings/data-elements/override/$', views.application_settings_data_elements_override, name='application.settings.data-elements.override'),
    url(r'^applications/(?P<application_id>\d+)/settings/services/$', views.application_settings_services, name='application.settings.services'),
    url(r'^applications/(?P<application_id>\d+)/settings/danger/$', views.application_settings_danger, name='application.settings.danger'),
    url(r'^applications/(?P<application_id>\d+)/delete/$', views.application_delete, name='application.delete'),

    # Environment
    url(r'^applications/(?P<application_id>\d+)/environments/add/$', views.environment_add, name='environment.add'),
    url(r'^environments/(?P<environment_id>\d+)/edit/$', views.environment_edit_general, name='environment.edit.general'),
    url(r'^environments/(?P<environment_id>\d+)/edit/locations/$', views.environment_edit_locations, name='environment.edit.locations'),
    url(r'^environments/(?P<environment_id>\d+)/edit/credentials/$', views.environment_edit_credentials, name='environment.edit.credentials'),
    url(r'^environments/(?P<environment_id>\d+)/edit/danger/$', views.environment_edit_danger, name='environment.edit.danger'),
    url(r'^environments/(?P<environment_id>\d+)/delete/$', views.environment_delete, name='environment.delete'),

    # Engagement
    url(r'^applications/(?P<application_id>\d+)/engagements/add/$', views.engagement_add, name='engagement.add'),
    url(r'^engagements/(?P<engagement_id>\d+)/$', views.engagement_detail, name='engagement.detail'),
    url(r'^engagements/(?P<engagement_id>\d+)/edit/$', views.engagement_edit, name='engagement.edit'),
    url(r'^engagements/(?P<engagement_id>\d+)/status/$', views.engagement_status, name='engagement.status'),
    url(r'^engagements/(?P<engagement_id>\d+)/delete/$', views.engagement_delete, name='engagement.delete'),
    url(r'^engagements/(?P<engagement_id>\d+)/comments/add/$', views.engagement_comment_add, name='engagement.comment.add'),



    # Activity Routes
    url(r'^engagements/(?P<engagement_id>\d+)/activities/add/$', views.activity_add, name='activity.add'),
    url(r'^activities/(?P<activity_id>\d+)/$', views.activity_detail, name='activity.detail'),
    url(r'^activities/(?P<activity_id>\d+)/edit/$', views.activity_edit, name='activity.edit'),
    url(r'^activities/(?P<activity_id>\d+)/status/$', views.activity_status, name='activity.status'),
    url(r'^activities/(?P<activity_id>\d+)/delete/$', views.activity_delete, name='activity.delete'),
    url(r'^activities/(?P<activity_id>\d+)/comments/add/$', views.activity_comment_add, name='activity.comment.add'),

    # People Routes
    url(r'^people/$', views.people_list, name='people.list'),
    url(r'^people/add/$', views.people_add, name='people.add'),
    url(r'^people/(?P<person_id>\d+)/$', views.people_detail, name='people.detail'),
)
