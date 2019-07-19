from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist

from rest_framework import serializers

from boh import models


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'is_active', 'last_login']
        read_only_fields = fields


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Tag
        fields = ['id', 'name', 'color', 'description']


class PersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Person
        fields = ['id', 'first_name', 'last_name', 'email', 'role', 'phone_work', 'phone_mobile', 'job_title']


class OrganizationSerializer(serializers.ModelSerializer):
    people = PersonSerializer(many = True, read_only = True)

    class Meta:
        model = models.Organization
        fields = ['id', 'name', 'description', 'people']


class ActivityTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ActivityType
        fields = ['id', 'name', 'documentation']


class ActivitySerializer(serializers.ModelSerializer):
    activity_type = ActivityTypeSerializer(read_only = True)
    users = UserSerializer(many = True, read_only = True)

    class Meta:
        model = models.Activity
        fields = ['id', 'status', 'description', 'open_date', 'close_date', 'duration', 'activity_type', 'engagement', 'users']


class DataElementSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.DataElement
        fields = ['id', 'name', 'description']


class ApplicationSerializer(serializers.ModelSerializer):
    class ApplicationCustomFieldValueSerializer(serializers.ModelSerializer):
        key = serializers.SerializerMethodField()

        class Meta:
            fields = ['id', 'key', 'value']
            model = models.ApplicationCustomFieldValue

        def get_key(self, custom_field_value):
            return custom_field_value.custom_field.key

    threadfix_metrics = serializers.SerializerMethodField()
    organization = OrganizationSerializer(read_only = True)
    tags = TagSerializer(many = True, read_only = True)
    data_elements = DataElementSerializer(many = True, read_only = True)
    custom_fields = ApplicationCustomFieldValueSerializer(source='applicationcustomfieldvalue_set', many = True, read_only = True)
    people = PersonSerializer(many = True, read_only = True)

    class Meta:
        model = models.Application
        fields = ['id', 'organization', 'name', 'description', 'business_criticality', 'platform', 'lifecycle', 'origin', 'user_records', 'revenue', 'external_audience', 'internet_accessible', 'threadfix_metrics', 'tags', 'data_elements', 'custom_fields', 'people']

    def get_threadfix_metrics(self, application):
        try:
            metrics = models.ThreadFixMetrics.objects.filter(application=application).latest()
            result = {
                'critical_count': metrics.critical_count,
                'high_count': metrics.high_count,
                'medium_count': metrics.medium_count,
                'low_count:': metrics.low_count,
                'informational_count': metrics.informational_count,
                'created_date': metrics.created_date
            }
            return result
        except ObjectDoesNotExist:
            return None


class EngagementSerializer(serializers.ModelSerializer):
    requestor = PersonSerializer(read_only = True)

    class Meta:
        model = models.Engagement
        fields = ['id', 'status', 'start_date', 'end_date', 'description', 'open_date', 'close_date', 'duration', 'requestor', 'application']


