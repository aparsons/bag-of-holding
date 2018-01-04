import django_filters

from django_filters import filters

from .models import Organization, Application, Vulnerability, VulnerabilityClass, Person


class ApplicationFilter(django_filters.FilterSet):
    name = filters.CharFilter(lookup_type='icontains')
    organization = filters.ModelMultipleChoiceFilter(queryset=Organization.objects.all())
    business_criticality = filters.MultipleChoiceFilter(choices=Application.BUSINESS_CRITICALITY_CHOICES)
    platform = filters.MultipleChoiceFilter(choices=Application.PLATFORM_CHOICES)
    lifecycle = filters.MultipleChoiceFilter(choices=Application.LIFECYCLE_CHOICES)
    origin = filters.MultipleChoiceFilter(choices=Application.ORIGIN_CHOICES)
    asvs_level = filters.MultipleChoiceFilter(choices=Application.ASVS_CHOICES)

    class Meta:
        model = Application
        fields = [
            'name', 'organization', 'business_criticality', 'platform', 'lifecycle', 'origin', 'external_audience',
            'internet_accessible', 'technologies', 'regulations', 'service_level_agreements', 'tags', 'asvs_level', 'data_elements'
        ]


class VulnerabilityFilter(django_filters.FilterSet):
    name = filters.CharFilter(lookup_type='icontains')
    affected_app = filters.ModelMultipleChoiceFilter(queryset=Application.objects.all())
    severity = filters.MultipleChoiceFilter(choices=Vulnerability.SEVERITY_CHOICES)
    status = filters.MultipleChoiceFilter(choices=Vulnerability.STATUS_CHOICES)
    reporter = filters.ModelMultipleChoiceFilter(queryset=Person.objects.all())
    detection_method = filters.MultipleChoiceFilter(choices=Vulnerability.DETECTION_METHOD_CHOICES)
    vulnerability_class = filters.ModelMultipleChoiceFilter(queryset=VulnerabilityClass.objects.all())

    class Meta:
        model = Vulnerability
        fields = [
            'name', 'affected_app', 'severity', 'vulnerability_class', 'status', 'reporter', 'tags',
            'vulnerability_class', 'detection_method'
        ]
