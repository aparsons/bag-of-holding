from django import forms

from tracker.models import Application, Engagement


class ApplicationAddForm(forms.ModelForm):
	class Meta:
		model = Application
		fields = ['name', 'description']


class ApplicationEditForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ['name', 'description', 'platform', 'lifecycle', 'origin', 'industry', 'business_criticality', 'external_audience', 'internet_accessible']


class ApplicationDeleteForm(forms.ModelForm):
	class Meta:
		model = Application
		fields = []


class EngagementAddForm(forms.ModelForm):
    class Meta:
        model = Engagement
        fields = ['start_date', 'end_date']
