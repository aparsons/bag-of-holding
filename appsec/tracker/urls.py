from django.conf.urls import patterns, include, url
from django.contrib.auth.decorators import login_required, permission_required

from tracker.views import ListApplicationView

urlpatterns = patterns('',


    url(r'^applications/$', login_required(ListApplicationView.as_view())),

)
