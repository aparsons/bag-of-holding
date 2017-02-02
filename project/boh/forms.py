from django import forms
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

from . import models


# Common

class PageSizeForm(forms.Form):
    PAGE_SIZE_CHOICES = (
        ('25', _('25 per page')),
        ('50', _('50 per page')),
        ('100', _('100 per page')),
        ('all', _('Everything'))
    )

    page_size = forms.ChoiceField(choices=PAGE_SIZE_CHOICES)


# Dashboard

class MetricsYearForm(forms.Form):

    def __init__(self, *args, **kwargs):
        super(MetricsYearForm, self).__init__(*args, **kwargs)

        engagement_years = models.Engagement.objects.distinct_years()
        activity_years = models.Activity.objects.distinct_years()
        years = engagement_years + list(set(activity_years) - set(engagement_years)) # Combine both lists
        years.sort(reverse=True)
        self.fields['year'] = forms.ChoiceField(label=_('Year'), choices=[('', _('All'))] + [(year, year) for year in years], required=False)


class EngagementCoverageReportForm(forms.Form):
    HTML_FORMAT = 'html'
    CSV_FORMAT = 'csv'
    FORMAT_CHOICES = (
        (HTML_FORMAT, 'HTML'),
        #(CSV_FORMAT, 'CSV'),
    )

    organizations = forms.ModelMultipleChoiceField(
        queryset=models.Organization.objects.all(),
        required=False
    )
    format = forms.ChoiceField(choices=FORMAT_CHOICES)


class ThreadFixSummaryReportForm(forms.Form):
    HTML_FORMAT = 'html'
    CSV_FORMAT = 'csv'
    FORMAT_CHOICES = (
        (HTML_FORMAT, 'HTML'),
        #(CSV_FORMAT, 'CSV'),
    )

    organizations = forms.ModelMultipleChoiceField(
        queryset=models.Organization.objects.all(),
        required=False
    )
    format = forms.ChoiceField(choices=FORMAT_CHOICES)

class AppSummaryReportForm(forms.Form):
    HTML_FORMAT = 'html'
    CSV_FORMAT = 'csv'
    FORMAT_CHOICES = (
        (HTML_FORMAT, 'HTML'),
        #(CSV_FORMAT, 'CSV'),
    )

    applications = forms.ModelMultipleChoiceField(
        queryset=models.Application.objects.all(),
        required=False
    )
    format = forms.ChoiceField(choices=FORMAT_CHOICES)


# User

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']


# Organization

class OrganizationAddForm(forms.ModelForm):
    class Meta:
        model = models.Organization
        fields = ['name', 'description']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 8})
        }


class OrganizationSettingsGeneralForm(forms.ModelForm):
    class Meta:
        model = models.Organization
        fields = ['name', 'description']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 8})
        }


class OrganizationSettingsPeopleForm(forms.ModelForm):
    class Meta:
        model = models.Organization
        fields = ['people']
        widgets = {
            'people': forms.SelectMultiple(attrs={'size': 15})
        }


class OrganizationDeleteForm(forms.ModelForm):
    class Meta:
        model = models.Organization
        fields = []


# ThreadFix

class ThreadFixForm(forms.ModelForm):
    class Meta:
        model = models.ThreadFix
        fields = ['name', 'host', 'api_key', 'verify_ssl']
        labels = {
            'api_key': _('API key'),
            'verify_ssl': _('Verify SSL certificate')
        }
        widgets = {
            'api_key': forms.PasswordInput(render_value=True)
        }


class ThreadFixApplicationImportForm(forms.Form):
    team_name = forms.CharField(max_length=128, widget=forms.HiddenInput())
    team_id = forms.IntegerField(min_value=0, max_value=2147483647, widget=forms.HiddenInput())
    application_id = forms.IntegerField(min_value=0, max_value=2147483647, widget=forms.HiddenInput())
    application_name = forms.CharField(max_length=128)
    organization = forms.ModelChoiceField(queryset=models.Organization.objects.all(), required=False)


class ThreadFixDeleteForm(forms.ModelForm):
    class Meta:
        model = models.ThreadFix
        fields = []


# Application

class ApplicationAddForm(forms.ModelForm):
    class Meta:
        model = models.Application
        fields = ['organization', 'name', 'description']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 8})
        }


class ApplicationSettingsGeneralForm(forms.ModelForm):
    class Meta:
        model = models.Application
        fields = ['name', 'description']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 8})
        }


class ApplicationSettingsOrganizationForm(forms.ModelForm):
    class Meta:
        model = models.Application
        fields = ['organization']


class ApplicationSettingsMetadataForm(forms.ModelForm):
    class Meta:
        model = models.Application
        fields = [
            'platform', 'lifecycle', 'origin', 'business_criticality', 'user_records', 'revenue', 'external_audience',
            'internet_accessible'
        ]


class ApplicationSettingsTechnologiesForm(forms.ModelForm):
    class Meta:
        model = models.Application
        fields = ['technologies']


class ApplicationSettingsRegulationsForm(forms.ModelForm):
    class Meta:
        model = models.Application
        fields = ['regulations']


class ApplicationSettingsTagsForm(forms.ModelForm):
    class Meta:
        model = models.Application
        fields = ['tags']


class ApplicationSettingsDataElementsForm(forms.ModelForm):
    class Meta:
        model = models.Application
        fields = ['data_elements']
        widgets = {
            'data_elements': forms.SelectMultiple(attrs={'size': 15})
        }


class ApplicationSettingsDCLOverrideForm(forms.ModelForm):
    class Meta:
        model = models.Application
        fields = ['override_dcl', 'override_reason']
        labels = {
            'override_dcl': 'Override data classification level'
        }
        widgets = {
            'override_reason': forms.Textarea(attrs={'rows': 3})
        }


class ApplicationSettingsServiceLevelAgreementForm(forms.ModelForm):
    class Meta:
        model = models.Application
        fields = ['service_level_agreements']


class ApplicationSettingsASVSForm(forms.ModelForm):
    class Meta:
        model = models.Application
        fields = ['asvs_level', 'asvs_level_percent_achieved', 'asvs_doc_url', 'asvs_level_target']
        labels = {
            'asvs_level': _('ASVS Level'),
            'asvs_level_percent_achieved': _('Percent Achived Towards Targeted Level'),
            'asvs_doc_url': _('ASVS Document'),
            'asvs_level_target': _('Target ASVS Level')
        }


class ApplicationSettingsThreadFixForm(forms.ModelForm):
    class Meta:
        model = models.Application
        fields = ['threadfix', 'threadfix_team_id', 'threadfix_application_id']
        labels = {
            'threadfix': _('ThreadFix Service'),
            'threadfix_team_id': _('Team ID'),
            'threadfix_application_id': _('Application ID')
        }


class ApplicationDeleteForm(forms.ModelForm):
    class Meta:
        model = models.Application
        fields = []


# Environment

class EnvironmentAddForm(forms.ModelForm):
    class Meta:
        model = models.Environment
        fields = ['environment_type', 'description', 'testing_approved']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3})
        }


class EnvironmentEditForm(forms.ModelForm):
    class Meta:
        model = models.Environment
        fields = ['environment_type', 'description', 'testing_approved']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3})
        }


class EnvironmentDeleteForm(forms.ModelForm):
    class Meta:
        model = models.Environment
        fields = []


class EnvironmentLocationAddForm(forms.ModelForm):
    class Meta:
        model = models.EnvironmentLocation
        fields = ['location', 'notes']
        widgets = {
            'notes': forms.Textarea(attrs={'rows': 3})
        }


class EnvironmentLocationEditForm(forms.ModelForm):
    class Meta:
        model = models.EnvironmentLocation
        fields = ['location', 'notes']
        widgets = {
            'notes': forms.Textarea(attrs={'rows': 3})
        }


# Engagement

class EngagementAddForm(forms.ModelForm):
    class Meta:
        model = models.Engagement
        fields = ['start_date', 'end_date', 'description', 'requestor']
        labels = {
            'start_date': 'Scheduled start date',
            'end_date': 'Scheduled end date'
        }
        widgets = {
            'description': forms.Textarea(attrs={'rows': 5})
        }

    def clean(self):
        cleaned = super(EngagementAddForm, self).clean()
        start_date = cleaned.get('start_date')
        end_date = cleaned.get('end_date')

        if start_date and end_date:
            if end_date < start_date:
                self.add_error('end_date', _("End date cannot be before start date."))


class EngagementEditForm(forms.ModelForm):
    class Meta:
        model = models.Engagement
        fields = ['status', 'start_date', 'end_date', 'description', 'requestor']
        labels = {
            'start_date': _('Scheduled start date'),
            'end_date': _('Scheduled end date')
        }
        widgets = {
            'description': forms.Textarea(attrs={'rows': 5})
        }

    def clean(self):
        cleaned = super(EngagementEditForm, self).clean()
        start_date = cleaned.get('start_date')
        end_date = cleaned.get('end_date')

        if start_date and end_date:
            if end_date < start_date:
                self.add_error('end_date', _("End date cannot be before start date."))


class EngagementStatusForm(forms.ModelForm):
    class Meta:
        model = models.Engagement
        fields = ['status']


class EngagementDeleteForm(forms.ModelForm):
    class Meta:
        model = models.Engagement
        fields = []


class EngagementCommentAddForm(forms.ModelForm):
    class Meta:
        model = models.EngagementComment
        fields = ['message']
        widgets = {
            'message': forms.Textarea(attrs={'rows': 3})
        }


# Activity

class ActivityAddForm(forms.ModelForm):
    class Meta:
        model = models.Activity
        fields = ['activity_type', 'description', 'users']
        labels = {
            'users': _('Assigned users')
        }
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3})
        }


class ActivityEditForm(forms.ModelForm):
    class Meta:
        model = models.Activity
        fields = ['status', 'activity_type', 'description', 'users']
        labels = {
            'users': _('Assigned users')
        }
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3})
        }


class ActivityStatusForm(forms.ModelForm):
    class Meta:
        model = models.Activity
        fields = ['status']


class ActivityCommentAddForm(forms.ModelForm):
    class Meta:
        model = models.ActivityComment
        fields = ['message']
        widgets = {
            'message': forms.Textarea(attrs={'rows': 3})
        }


class ActivityDeleteForm(forms.ModelForm):
    class Meta:
        model = models.Activity
        fields = []


# Person

class PersonForm(forms.ModelForm):
    class Meta:
        model = models.Person
        fields = ['first_name', 'last_name', 'email', 'phone_work', 'phone_mobile', 'job_title', 'role']


class PersonDeleteForm(forms.ModelForm):
    class Meta:
        model = models.Person
        fields = []


# Relation

class PersonRelationForm(forms.ModelForm):
    """For relating a person to an application."""
    class Meta:
        model = models.Relation
        fields = ['person', 'owner', 'emergency', 'notes']
        labels = {
            'owner': _('Application Owner'),
            'emergency': _('Emergency Contact')
        }
        widgets = {
            'notes': forms.Textarea(attrs={'rows': 3})
        }


class RelationDeleteForm(forms.ModelForm):
    class Meta:
        model = models.Relation
        fields = []


# Application Tag

class ApplicationTagForm(forms.ModelForm):
    class Meta:
        model = models.Tag
        fields = ['name', 'description', 'color']


class ApplicationTagDeleteForm(forms.ModelForm):
    class Meta:
        model = models.Tag
        fields = []


# Activity Type

class ActivityTypeForm(forms.ModelForm):
    class Meta:
        model = models.ActivityType
        fields = ['name', 'documentation']


class ActivityTypeDeleteForm(forms.ModelForm):
    class Meta:
        model = models.ActivityType
        fields = []
