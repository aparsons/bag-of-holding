import django_filters

from django_filters import filters

from .models import Organization, Application


class ApplicationFilter(django_filters.FilterSet):

    PLATFORM_CHOICES = (
        (None, 'Any'),
        (Application.WEB_PLATFORM, 'Web'),
        (Application.DESKTOP_PLATFORM, 'Desktop'),
        (Application.MOBILE_PLATFORM, 'Mobile'),
        (Application.WEB_SERVICE_PLATFORM, 'Web Service'),
    )

    LIFECYCLE_CHOICES = (
        (None, 'Any'),
        (Application.IDEA_LIFECYCLE, 'Idea'),
        (Application.EXPLORE_LIFECYCLE, 'Explore'),
        (Application.VALIDATE_LIFECYCLE, 'Validate'),
        (Application.GROW_LIFECYCLE, 'Grow'),
        (Application.SUSTAIN_LIFECYCLE, 'Sustain'),
        (Application.RETIRE_LIFECYCLE, 'Retire'),
    )

    ORIGIN_CHOICES = (
        (None, 'Any'),
        (Application.THIRD_PARTY_LIBRARY_ORIGIN, 'Third Party Library'),
        (Application.PURCHASED_ORIGIN, 'Purchased'),
        (Application.CONTRACTOR_ORIGIN, 'Contractor'),
        (Application.INTERNALLY_DEVELOPED_ORIGIN, 'Internally Developed'),
        (Application.OPEN_SOURCE_ORIGIN, 'Open Source'),
        (Application.OUTSOURCED_ORIGIN, 'Outsourced'),
    )

    name = filters.CharFilter(lookup_type='icontains')
    organization = filters.ModelMultipleChoiceFilter(queryset=Organization.objects.all())
    business_criticality = filters.MultipleChoiceFilter(choices=Application.BUSINESS_CRITICALITY_CHOICES)
    platform = filters.MultipleChoiceFilter(choices=Application.PLATFORM_CHOICES)
    lifecycle = filters.MultipleChoiceFilter(choices=Application.LIFECYCLE_CHOICES)
    origin = filters.MultipleChoiceFilter(choices=Application.LIFECYCLE_CHOICES)

    class Meta:
        model = Application
        fields = ['name', 'organization', 'business_criticality', 'platform', 'lifecycle', 'origin', 'tags']

    def __init__(self, *args, **kwargs):
        super(ApplicationFilter, self).__init__(*args, **kwargs)
        #self.filters['organization'].extra.update({'empty_label': 'All Organizations'})
