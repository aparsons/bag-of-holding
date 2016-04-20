from django.conf import settings
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.views import login, logout



base_urlpatterns = [
    url(r'^', include('boh.urls', namespace='boh')),

    url(r'^api/', include('boh_api.urls', namespace='boh_api')),

    #url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    #url(r'^2/', include('boh_ui.urls', namespace='boh_ui')),
    #url(r'^requests/', include('pearson_requests.urls', namespace='pearson_requests')),

    url(r'^dcl/', include('pearson_dcl.urls', namespace='pearson_dcl')),

    url(r'^accounts/login/$', login, name='login'),
    url(r'^accounts/logout/$', logout, name='logout'),

    url(r'^admin/', include(admin.site.urls)),
]

# url(r'^accounts/change-password/$', 'django.contrib.auth.views.password_change', name='password_change'),
# url(r'^accounts/change-password/done/$', 'django.contrib.auth.views.password_change_done', name='password_change_done'),
# url(r'^', include('django.contrib.auth.urls')),

# Apply URL_PREFIX setting to all urls
if settings.URL_PREFIX:
    urlpatterns = [
        url(r'^' + settings.URL_PREFIX, include(base_urlpatterns)),
    ]
else:
    urlpatterns = base_urlpatterns

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
