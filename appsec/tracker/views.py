from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import Http404
from django.shortcuts import render

from tracker.models import Application

# Create your views here.

@login_required
def list_applications(request):
    application_list = Application.objects.all()
    paginator = Paginator(application_list, 3)

    page = request.GET.get('page')
    try:
        applications = paginator.page(page)
    except PageNotAnInteger:
        applications = paginator.page(1)
    except EmptyPage:
        applications = paginator.page(paginator.num_pages)

    return render(request, 'tracker/applications/list.html', {"applications": applications})

@login_required
def application_detail(request, application_id):
    try:
        application = Application.objects.get(pk=application_id)
    except Application.DoesNotExist:
        raise Http404("Application does not exist")
    return render(request, 'tracker/applications/detail.html', {"application": application})
