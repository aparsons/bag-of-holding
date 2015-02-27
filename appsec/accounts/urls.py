from django.conf.urls import patterns, url

from accounts import views

urlpatterns = patterns('',

    # Auth Routes
    url(r'^login/$', 'django.contrib.auth.views.login', name='login'),
    url(r'^logout/$', 'django.contrib.auth.views.logout', name='logout'),

	# Settings Routes
    url(r'^profile/$', views.settings_profile, name='settings.profile'),
    url(r'^settings/$', views.settings_account_settings, name='settings.account.settings'),
    url(r'^notifications/$', views.settings_notifications, name='settings.notifications'),

)
