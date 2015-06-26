from django import forms
from django.utils.translation import ugettext as _

from boh import models


class EmailForm(forms.Form):
    email = forms.EmailField()


class PersonForm(forms.ModelForm):
    class Meta:
        model = models.Person
        fields = ['first_name', 'last_name', 'email', 'phone_work', 'phone_mobile', 'job_title', 'role']


class ApplicationForm(forms.Form):
    application = forms.ModelChoiceField(queryset=models.Application.objects.requestable())
    activity_types = forms.ModelMultipleChoiceField(queryset=models.ActivityType.objects.requestable())
    start_date = forms.DateField(help_text='The date the engagement is scheduled to begin.')
    end_date = forms.DateField(help_text='The date the engagement is scheduled to complete.')

class ConfirmForm(forms.Form):
    pass
