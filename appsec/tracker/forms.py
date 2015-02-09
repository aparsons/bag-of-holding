from django import forms

from tracker.models import Application, Engagement

# Deprecated
class ApplicationEditForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ['name', 'description', 'platform', 'lifecycle', 'origin', 'industry', 'business_criticality', 'external_audience', 'internet_accessible']


class ApplicationAddForm(forms.ModelForm):
	class Meta:
		model = Application
		fields = ['name', 'description']


class ApplicationDeleteForm(forms.ModelForm):
	class Meta:
		model = Application
		fields = ['id']


class EngagementAddForm(forms.ModelForm):
    class Meta:
        model = Engagement
        fields = ['start_date', 'end_date']
