from django import forms

from tracker.models import Application


class AddApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ['name', 'description', 'platform', 'lifecycle', 'origin', 'industry', 'business_criticality', 'external_audience', 'internet_accessible']
