from django import forms
from django.utils.translation import ugettext as _

from boh.models import Application, Person

from . import models


class EmailForm(forms.Form):
    email = forms.EmailField()


class PersonForm(forms.ModelForm):
    class Meta:
        model = Person
        fields = ['first_name', 'last_name', 'email', 'phone_work', 'phone_mobile', 'job_title', 'role']


class ApplicationForm(forms.Form):
    application = forms.ModelChoiceField(queryset=Application.objects.requestable())
    service_bundle = forms.ModelChoiceField(queryset=models.ServiceBundle.objects.all())
    start_date = forms.DateField()
    end_date = forms.DateField()


class ConfirmForm(forms.Form):
    pass
