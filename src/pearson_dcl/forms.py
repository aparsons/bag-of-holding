from django import forms

from boh.models import DataElement


class DCLForm(forms.Form):
    data_elements = forms.ModelMultipleChoiceField(queryset=DataElement.objects.all())
