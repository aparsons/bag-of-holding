import django_filters

from .models import Organization, Application


class ApplicationFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains')
    organization = django_filters.ModelMultipleChoiceFilter(queryset=Organization.objects.all())
    business_criticality = django_filters.MultipleChoiceFilter(choices=Application.BUSINESS_CRITICALITY_CHOICES)
    platform = django_filters.MultipleChoiceFilter(choices=Application.PLATFORM_CHOICES)
    lifecycle = django_filters.MultipleChoiceFilter(choices=Application.LIFECYCLE_CHOICES)
    origin = django_filters.MultipleChoiceFilter(choices=Application.ORIGIN_CHOICES)
    asvs_level = django_filters.MultipleChoiceFilter(choices=Application.ASVS_CHOICES)

    class Meta:
        model = Application
        fields = [
            'name', 'organization', 'business_criticality', 'platform', 'lifecycle', 'origin', 'external_audience',
            'internet_accessible', 'technologies', 'regulations', 'service_level_agreements', 'tags', 'asvs_level'
        ]
