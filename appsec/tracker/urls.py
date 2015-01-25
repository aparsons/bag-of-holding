from django.conf.urls import patterns, include, url
from django.contrib.auth.decorators import login_required

from tracker import views

urlpatterns = patterns('',

    url(r'^applications/$', login_required(views.list_applications), name='applications'),

)
