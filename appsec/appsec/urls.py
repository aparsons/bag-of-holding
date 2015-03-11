from django.conf import settings
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.views.generic.base import RedirectView

from tracker.views import dashboard_personal, management_services, management_users

base_urlpatterns = patterns('',
    url(r'^$', RedirectView.as_view(pattern_name='tracker:dashboard.personal')),

    url(r'^tracker/', include('tracker.urls', namespace="tracker")),
    url(r'^accounts/', include('accounts.urls', namespace="accounts")),

    url(r'^admin/', include(admin.site.urls)),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns = patterns('',
  url(r'^' + settings.URL_PREFIX, include(base_urlpatterns))
)
