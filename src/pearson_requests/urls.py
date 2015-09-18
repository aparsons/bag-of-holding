from django.conf.urls import patterns, include, url

from . import views, wizards


erw = wizards.ServiceRequestWizard.as_view(wizards.ServiceRequestWizard.Forms, condition_dict=wizards.ServiceRequestWizard.Conditions)

urlpatterns = patterns('',
    url(r'^$', erw, name='index'),
    url(r'^success/$', views.success, name='success'),

    url(r'^status/(?P<token>[^/]+)/$', views.status, name='status'),
    url(r'^status/(?P<token>[^/]+)/settings$', views.status_settings, name='status.settings'),
    url(r'^status/(?P<token>[^/]+)/comment', views.status_comment, name='status.comment'),
    url(r'^status/(?P<token>[^/]+)/cancel', views.status_cancel, name='status.cancel'),
)
