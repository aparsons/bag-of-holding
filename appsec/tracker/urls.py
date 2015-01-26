from django.conf.urls import patterns, include, url
from django.contrib.auth.decorators import login_required

from tracker import views

urlpatterns = patterns('',

    url(r'^applications/$', views.list_applications),
    url(r'^applications/(?P<application_id>\d+)/$', views.application_detail),

)
