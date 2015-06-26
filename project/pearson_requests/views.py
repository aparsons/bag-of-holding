from django.shortcuts import render


def external_request_success(request):
    return render(request, 'pearson_requests/wizards/external_request/success.html', {})
