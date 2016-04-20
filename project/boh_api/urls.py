from django.conf.urls import include, url

from rest_framework import routers

from . import viewsets


router = routers.DefaultRouter()
router.register(r'organizations', viewsets.OrganizationViewSet)
router.register(r'applications', viewsets.ApplicationViewSet)
router.register(r'tags', viewsets.TagViewSet)
router.register(r'people', viewsets.PersonViewSet)

urlpatterns = [
    url(r'^v0/', include(router.urls), name='v0'),
    #url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]
