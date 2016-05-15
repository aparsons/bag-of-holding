from django.core.exceptions import ObjectDoesNotExist

from rest_framework import serializers

from boh import models


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Tag


class OrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Organization


class ApplicationCustomFieldValueSerializer(serializers.ModelSerializer):
    key = serializers.SerializerMethodField()

    class Meta:
        fields = ['id', 'key', 'value']
        model = models.ApplicationCustomFieldValue

    def get_key(self, custom_field_value):
        return custom_field_value.custom_field.key


class ApplicationSerializer(serializers.ModelSerializer):
    threadfix_metrics = serializers.SerializerMethodField()
    organization = OrganizationSerializer(read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    custom_fields = ApplicationCustomFieldValueSerializer(source='applicationcustomfieldvalue_set', many=True, read_only=True)

    class Meta:
        model = models.Application
        fields = ['id', 'organization', 'name', 'description', 'business_criticality', 'platform', 'lifecycle', 'origin', 'user_records', 'revenue', 'external_audience', 'internet_accessible', 'threadfix_metrics', 'tags', 'custom_fields', 'people']

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


class PersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Person
