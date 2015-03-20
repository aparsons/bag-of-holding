from django.conf import settings
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.contrib import admin

base_urlpatterns = patterns('',
    url(r'^', include('boh.urls', namespace='boh')),

    url(r'^accounts/login/$', 'django.contrib.auth.views.login', name='login'),
    url(r'^accounts/logout/$', 'django.contrib.auth.views.logout', name='logout'),
    #url(r'^accounts/change-password/$', 'django.contrib.auth.views.password_change', name='password_change'),
    #url(r'^accounts/change-password/done/$', 'django.contrib.auth.views.password_change_done', name='password_change_done'),
    #url(r'^', include('django.contrib.auth.urls')),
    url(r'^admin/', include(admin.site.urls)),
)

urlpatterns = patterns('',
  url(r'^' + settings.URL_PREFIX, include(base_urlpatterns)),
)

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
