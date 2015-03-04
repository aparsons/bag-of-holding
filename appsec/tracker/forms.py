from django import forms

from tracker.models import Organization, Application, Environment, EnvironmentLocation, Engagement, EngagementComment, Activity, ActivityComment, Person

# Organization

class OrganizationAddForm(forms.ModelForm):
    class Meta:
        model = Organization
        fields = ['name', 'description']


# Application


class ApplicationAddForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ['organization', 'name', 'description']


class ApplicationSettingsGeneralForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ['organization', 'name', 'description']


class ApplicationSettingsMetadataForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ['platform', 'lifecycle', 'origin', 'industry', 'business_criticality', 'external_audience', 'internet_accessible']


class ApplicationSettingsTagsForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ['tags']


class ApplicationDeleteForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = []


# Environment


class EnvironmentAddForm(forms.ModelForm):
    class Meta:
        model = Environment
        fields = ['environment_type', 'description', 'testing_approved']


class EnvironmentEditForm(forms.ModelForm):
    class Meta:
        model = Environment
        fields = ['environment_type', 'description', 'testing_approved']


class EnvironmentLocationAddForm(forms.ModelForm):
    class Meta:
        model = EnvironmentLocation
        fields = ['location', 'notes']


# Engagement


class EngagementAddForm(forms.ModelForm):
    class Meta:
        model = Engagement
        fields = ['start_date', 'end_date']
        labels = {
            'start_date': 'Scheduled start date',
            'end_date': 'Scheduled end date'
        }

    def clean(self):
        cleaned = super(EngagementEditForm, self).clean()
        start_date = cleaned.get('start_date')
        end_date = cleaned.get('end_date')

        if start_date and end_date:
            if end_date < start_date:
                self.add_error('end_date', "End date cannot be before start date.")


class EngagementEditForm(forms.ModelForm):
    class Meta:
        model = Engagement
        fields = ['status', 'start_date', 'end_date']
        labels = {
            'start_date': 'Scheduled start date',
            'end_date': 'Scheduled end date'
        }

    def clean(self):
        cleaned = super(EngagementEditForm, self).clean()
        start_date = cleaned.get('start_date')
        end_date = cleaned.get('end_date')

        if start_date and end_date:
            if end_date < start_date:
                self.add_error('end_date', "End date cannot be before start date.")


class EngagementDeleteForm(forms.ModelForm):
    class Meta:
        model = Engagement
        fields = []


class EngagementCommentAddForm(forms.ModelForm):
    class Meta:
        model = EngagementComment
        fields = ['message']
        widgets = {
            'message': forms.Textarea(attrs = {'rows': 3})
        }


# Activity


class ActivityAddForm(forms.ModelForm):
    class Meta:
        model = Activity
        fields = ['activity_type', 'description', 'users']
        labels = {
            'users': 'Assigned users'
        }


class ActivityEditForm(forms.ModelForm):
    class Meta:
        model = Activity
        fields = ['status', 'activity_type', 'description', 'users']
        labels = {
            'users': 'Assigned users'
        }


class ActivityDeleteForm(forms.ModelForm):
    class Meta:
        model = Activity
        fields = []


class ActivityCommentAddForm(forms.ModelForm):
    class Meta:
        model = ActivityComment
        fields = ['message']
        widgets = {
            'message': forms.Textarea(attrs = {'rows': 3})
        }


# Person


class PersonAddForm(forms.ModelForm):
    class Meta:
        model = Person
        fields = ['first_name', 'last_name', 'email', 'phone_work', 'phone_mobile']
