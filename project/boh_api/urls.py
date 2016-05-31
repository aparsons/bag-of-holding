from django.conf.urls import include, url

from rest_framework import routers

from . import viewsets


router = routers.DefaultRouter()
router.register(r'organizations', viewsets.OrganizationViewSet)
router.register(r'applications', viewsets.ApplicationViewSet)
router.register(r'tags', viewsets.TagViewSet)
router.register(r'people', viewsets.PersonViewSet)
router.register(r'engagements', viewsets.EngagementViewSet)
router.register(r'activities', viewsets.ActivityViewSet)
router.register(r'activities_types', viewsets.ActivityTypeViewSet)
router.register(r'users', viewsets.UserViewSet)

urlpatterns = [
    url(r'^v0/', include(router.urls), name='v0'),
    #url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]
