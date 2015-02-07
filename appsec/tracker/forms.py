from django import forms

from tracker.models import Application, Engagement


class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ['name', 'description', 'platform', 'lifecycle', 'origin', 'industry', 'business_criticality', 'external_audience', 'internet_accessible']


class EngagementForm(forms.ModelForm):
    class Meta:
        model = Engagement
        fields = ['start_date', 'end_date']
