from django.shortcuts import render

from boh import helpers
from boh.models import DataElement

from . import forms


def index(request):
    dsv = None
    dcl = None

    dcl_form = forms.DCLForm(request.GET or None)
    if dcl_form.is_valid():
        dsv = helpers.data_sensitivity_value(dcl_form.cleaned_data['data_elements'])
        dcl = helpers.data_classification_level(dsv)

    data_elements = DataElement.objects.all()

    return render(request, 'pearson_dcl/index.html', {
        'dcl_form': dcl_form,
        'dsv': dsv,
        'dcl': dcl,
        'data_elements': data_elements
    })
