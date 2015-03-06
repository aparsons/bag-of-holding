from django.conf import settings
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.decorators import login_required

from tracker.views import dashboard_detail, management_services, management_users

base_urlpatterns = patterns('',
    url(r'^$', dashboard_detail, name='dashboard'),

    url(r'^manage/services/$', management_services, name='management.services'),
    url(r'^manage/users/$', management_users, name='management.users'),

    url(r'^accounts/', include('accounts.urls', namespace="accounts")),
    url(r'^tracker/', include('tracker.urls', namespace="tracker")),

    url(r'^admin/', include(admin.site.urls)),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns = patterns('',
  url(r'^' + settings.URL_PREFIX, include(base_urlpatterns))
)
