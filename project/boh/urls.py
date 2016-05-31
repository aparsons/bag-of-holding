from django.conf.urls import url

from . import views

urlpatterns = [

    # Dashboard
    url(r'^$', views.dashboard_personal, name='dashboard.personal'),
    url(r'^team/$', views.dashboard_team, name='dashboard.team'),
    url(r'^metrics/$', views.dashboard_metrics, name='dashboard.metrics'),
    url(r'^reports/$', views.dashboard_reports, name='dashboard.reports'),
    url(r'^reports/download/$', views.dashboard_reports_download, name='dashboard.reports.download'),

    # Management
    url(r'^manage/$', views.management_overview, name='management.overview'),
    url(r'^manage/tags/$', views.management_application_tags, name='management.tags'),
    url(r'^manage/tags/add/$', views.management_application_tags_add, name='management.tags.add'),
    url(r'^manage/tags/(?P<tag_id>\d+)/edit/$', views.management_application_tags_edit, name='management.tags.edit'),
    url(r'^manage/tags/(?P<tag_id>\d+)/delete/$', views.management_application_tags_delete, name='management.tags.delete'),
    url(r'^manage/activity-types/$', views.management_activity_types, name='management.activity_types'),
    url(r'^manage/activity-types/add/$', views.management_activity_types_add, name='management.activity_types.add'),
    url(r'^manage/activity-types/(?P<activity_type_id>\d+)/documentation/$', views.management_activity_types_documentation, name='management.activity_types.documentation'),
    url(r'^manage/activity-types/(?P<activity_type_id>\d+)/edit/$', views.management_activity_types_edit, name='management.activity_types.edit'),
    url(r'^manage/activity-types/(?P<activity_type_id>\d+)/delete/$', views.management_activity_types_delete, name='management.activity_types.delete'),
    url(r'^manage/services/$', views.management_services, name='management.services'),
    url(r'^manage/services/threadfix/add/', views.management_services_threadfix_add, name='management.services.threadfix.add'),
    url(r'^manage/services/threadfix/(?P<threadfix_id>\d+)/edit/', views.management_services_threadfix_edit, name='management.services.threadfix.edit'),
    url(r'^manage/services/threadfix/(?P<threadfix_id>\d+)/test/', views.management_services_threadfix_test, name='management.services.threadfix.test'),
    url(r'^manage/services/threadfix/(?P<threadfix_id>\d+)/import/', views.management_services_threadfix_import, name='management.services.threadfix.import'),
    url(r'^manage/services/threadfix/(?P<threadfix_id>\d+)/delete/', views.management_services_threadfix_delete, name='management.services.threadfix.delete'),
    url(r'^manage/users/$', views.management_users, name='management.users'),

    # User
    url(r'^accounts/profile/$', views.user_profile, name='user.profile'),
    url(r'^accounts/password/$', views.user_change_password, name='user.change_password'),

    # Organization
    url(r'^organizations/add/$', views.organization_add, name='organization.add'),
    url(r'^organizations/(?P<organization_id>\d+)/$', views.organization_overview, name='organization.overview'),
    url(r'^organizations/(?P<organization_id>\d+)/applications/$', views.organization_applications, name='organization.applications'),
    url(r'^organizations/(?P<organization_id>\d+)/people/$', views.organization_people, name='organization.people'),
    url(r'^organizations/(?P<organization_id>\d+)/settings/$', views.organization_settings_general, name='organization.settings.general'),
    url(r'^organizations/(?P<organization_id>\d+)/settings/people/$', views.organization_settings_people, name='organization.settings.people'),
    url(r'^organizations/(?P<organization_id>\d+)/settings/danger/$', views.organization_settings_danger, name='organization.settings.danger'),

    # Application
    url(r'^applications/$', views.application_list, name='application.list'),
    url(r'^applications/add/$', views.application_add, name='application.add'),
    url(r'^applications/(?P<application_id>\d+)/$', views.application_overview, name='application.overview'),
    url(r'^applications/(?P<application_id>\d+)/engagements/$', views.application_engagements, name='application.engagements'),
    url(r'^applications/(?P<application_id>\d+)/environments/$', views.application_environments, name='application.environments'),
    url(r'^applications/(?P<application_id>\d+)/people/$', views.application_people, name='application.people'),
    url(r'^applications/(?P<application_id>\d+)/people/add/$', views.application_people_add, name='application.people.add'),
    url(r'^applications/(?P<application_id>\d+)/people/(?P<relation_id>\d+)/edit/$', views.application_people_edit, name='application.people.edit'),
    url(r'^applications/(?P<application_id>\d+)/people/(?P<relation_id>\d+)/delete/$', views.application_people_delete, name='application.people.delete'),
    url(r'^applications/(?P<application_id>\d+)/settings/$', views.application_settings_general, name='application.settings.general'),
    url(r'^applications/(?P<application_id>\d+)/settings/metadata/$', views.application_settings_metadata, name='application.settings.metadata'),
    url(r'^applications/(?P<application_id>\d+)/settings/data-elements/$', views.application_settings_data_elements, name='application.settings.data-elements'),
    url(r'^applications/(?P<application_id>\d+)/settings/data-elements/override/$', views.application_settings_data_elements_override, name='application.settings.data-elements.override'),
    url(r'^applications/(?P<application_id>\d+)/settings/service-level-agreements/$', views.application_settings_service_level_agreements, name='application.settings.service-level-agreements'),
    url(r'^applications/(?P<application_id>\d+)/settings/owasp/$', views.application_settings_owasp_asvs, name='application.settings.owasp-asvs'),
    url(r'^applications/(?P<application_id>\d+)/settings/services/$', views.application_settings_services, name='application.settings.services'),
    url(r'^applications/(?P<application_id>\d+)/settings/custom-fields/$', views.application_settings_custom_fields, name='application.settings.custom-fields'),
    url(r'^applications/(?P<application_id>\d+)/settings/danger/$', views.application_settings_danger, name='application.settings.danger'),

    # Environment
    url(r'^applications/(?P<application_id>\d+)/environments/add/$', views.environment_add, name='environment.add'),
    url(r'^environments/(?P<environment_id>\d+)/edit/$', views.environment_edit_general, name='environment.edit.general'),
    url(r'^environments/(?P<environment_id>\d+)/edit/locations/$', views.environment_edit_locations, name='environment.edit.locations'),
    url(r'^environments/(?P<environment_id>\d+)/edit/credentials/$', views.environment_edit_credentials, name='environment.edit.credentials'),
    url(r'^environments/(?P<environment_id>\d+)/edit/danger/$', views.environment_edit_danger, name='environment.edit.danger'),

    # Engagement
    url(r'^applications/(?P<application_id>\d+)/engagements/add/$', views.engagement_add, name='engagement.add'),
    url(r'^engagements/(?P<engagement_id>\d+)/$', views.engagement_detail, name='engagement.detail'),
    url(r'^engagements/(?P<engagement_id>\d+)/edit/$', views.engagement_edit, name='engagement.edit'),
    url(r'^engagements/(?P<engagement_id>\d+)/status/$', views.engagement_status, name='engagement.status'),
    url(r'^engagements/(?P<engagement_id>\d+)/delete/$', views.engagement_delete, name='engagement.delete'),
    url(r'^engagements/(?P<engagement_id>\d+)/comments/add/$', views.engagement_comment_add, name='engagement.comment.add'),

    # Activity
    url(r'^engagements/(?P<engagement_id>\d+)/activities/add/$', views.activity_add, name='activity.add'),
    url(r'^activities/(?P<activity_id>\d+)/$', views.activity_detail, name='activity.detail'),
    url(r'^activities/(?P<activity_id>\d+)/edit/$', views.activity_edit, name='activity.edit'),
    url(r'^activities/(?P<activity_id>\d+)/status/$', views.activity_status, name='activity.status'),
    url(r'^activities/(?P<activity_id>\d+)/delete/$', views.activity_delete, name='activity.delete'),
    url(r'^activities/(?P<activity_id>\d+)/comments/add/$', views.activity_comment_add, name='activity.comment.add'),

    # People
    url(r'^people/$', views.person_list, name='person.list'),
    url(r'^people/add/$', views.person_add, name='person.add'),
    url(r'^people/(?P<person_id>\d+)/$', views.person_detail, name='person.detail'),
    url(r'^people/(?P<person_id>\d+)/edit/$', views.person_edit, name='person.edit'),
    url(r'^people/(?P<person_id>\d+)/delete/$', views.person_delete, name='person.delete'),
]
