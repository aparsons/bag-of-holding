from django.conf.urls import patterns, include, url

from . import views, wizards


erw = wizards.ExternalRequestWizard.as_view(wizards.ExternalRequestWizard.Forms, condition_dict=wizards.ExternalRequestWizard.Conditions)

urlpatterns = patterns('',
    url(r'^$', erw, name='service_request'),
    url(r'^success/$', views.service_request_success, name='service_request_success'),
    url(r'^status/(?P<token>[^/]+)/$', views.service_requests_status, name='service_request_status'),
)
