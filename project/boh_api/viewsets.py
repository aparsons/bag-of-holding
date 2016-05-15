from django.contrib.auth import get_user_model

from rest_framework import viewsets

from boh import models

from . import serializers


class OrganizationViewSet(viewsets.ModelViewSet):
    queryset = models.Organization.objects.all()
    serializer_class = serializers.OrganizationSerializer


class ApplicationViewSet(viewsets.ModelViewSet):
    queryset = models.Application.objects.all()
    serializer_class = serializers.ApplicationSerializer


class TagViewSet(viewsets.ModelViewSet):
    queryset = models.Tag.objects.all()
    serializer_class = serializers.TagSerializer


class PersonViewSet(viewsets.ModelViewSet):
    queryset = models.Person.objects.all()
    serializer_class = serializers.PersonSerializer


class EngagementViewSet(viewsets.ModelViewSet):
    queryset = models.Engagement.objects.all()
    serializer_class = serializers.EngagementSerializer


class ActivityViewSet(viewsets.ModelViewSet):
    queryset = models.Activity.objects.all()
    serializer_class = serializers.ActivitySerializer


class ActivityTypeViewSet(viewsets.ModelViewSet):
    queryset = models.ActivityType.objects.all()
    serializer_class = serializers.ActivityTypeSerializer


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = get_user_model().objects.all()
    serializer_class = serializers.UserSerializer
