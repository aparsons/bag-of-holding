from django import forms

from tracker.models import Application


class AddApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
