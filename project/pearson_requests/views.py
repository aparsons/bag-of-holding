from django.shortcuts import get_object_or_404, render, redirect
from django.views.decorators.http import require_http_methods

from boh.models import ServiceRequest


@require_http_methods(['GET'])
def service_request_success(request):
    return render(request, 'pearson_requests/wizards/external_request/success.html')


@require_http_methods(['GET'])
def service_requests_status(request, token):
    service_request = get_object_or_404(ServiceRequest, token=token)

    return render(request, 'pearson_requests/wizards/external_request/status.html', {
        'service_request': service_request
    })

