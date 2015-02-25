from django.conf.urls import patterns, url

from accounts import views

urlpatterns = patterns('',

    url(r'^login/$', 'django.contrib.auth.views.login', name='login'),
    url(r'^logout/$', 'django.contrib.auth.views.logout', name='logout'),

	# Application Routes
    url(r'^profile/$', views.profile_edit, name='profile.edit'),


)
