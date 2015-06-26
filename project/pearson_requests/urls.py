from django.conf.urls import patterns, include, url

from . import views, wizards


erw = wizards.ExternalRequestWizard.as_view(wizards.ExternalRequestWizard.Forms, condition_dict=wizards.ExternalRequestWizard.Conditions)

urlpatterns = patterns('',
    url(r'^$', erw, name='external_request'),
    url(r'^success/$', views.external_request_success, name='external_request_success'),
)
