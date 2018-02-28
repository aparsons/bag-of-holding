import django_filters
from .models import Organization, Application, Vulnerability, VulnerabilityClass, Person


class ApplicationFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains')
    organization = django_filters.ModelMultipleChoiceFilter(queryset=Organization.objects.all())
    business_criticality = django_filters.MultipleChoiceFilter(choices=Application.BUSINESS_CRITICALITY_CHOICES)
    platform = django_filters.MultipleChoiceFilter(choices=Application.PLATFORM_CHOICES)
    lifecycle = django_filters.MultipleChoiceFilter(choices=Application.LIFECYCLE_CHOICES)
    origin = django_filters.MultipleChoiceFilter(choices=Application.ORIGIN_CHOICES)
    asvs_level = django_filters.MultipleChoiceFilter(choices=Application.ASVS_CHOICES)

    def count(self):
        count = 0
        if self.queryset is not None:
            count = len(self.queryset)
        return count

    def __getitem__(self, item):
        return self.queryset[item]

    class Meta:
        model = Application
        fields = [
            'name', 'organization', 'business_criticality', 'platform', 'lifecycle', 'origin', 'external_audience',
            'internet_accessible', 'technologies', 'regulations', 'service_level_agreements', 'tags', 'asvs_level', 'data_elements'
        ]


class VulnerabilityFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains')
    affected_app = django_filters.ModelMultipleChoiceFilter(queryset=Application.objects.all())
    severity = django_filters.MultipleChoiceFilter(choices=Vulnerability.SEVERITY_CHOICES)
    status = django_filters.MultipleChoiceFilter(choices=Vulnerability.STATUS_CHOICES)
    reporter = django_filters.ModelMultipleChoiceFilter(queryset=Person.objects.all())
    detection_method = django_filters.MultipleChoiceFilter(choices=Vulnerability.DETECTION_METHOD_CHOICES)
    vulnerability_classes = django_filters.ModelMultipleChoiceFilter(queryset=VulnerabilityClass.objects.all())

    def count(self):
        count = 0
        if self.queryset is not None:
            count = len(self.queryset)
        return count

    def __getitem__(self, item):
        return self.queryset[item]

    class Meta:
        model = Vulnerability
        fields = [
            'name', 'affected_app', 'severity', 'vulnerability_classes', 'status', 'reporter', 'tags',
            'detection_method'
        ]
