from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import Http404
from django.shortcuts import render, redirect

from tracker.models import Application, Engagement
from tracker.forms import ApplicationForm

# Create your views here.

@login_required
def list_applications(request):
    application_list = Application.objects.all()
    paginator = Paginator(application_list, 20)

    page = request.GET.get('page')
    try:
        applications = paginator.page(page)
    except PageNotAnInteger:
        applications = paginator.page(1)
    except EmptyPage:
        applications = paginator.page(paginator.num_pages)

    return render(request, 'tracker/applications/list.html', {'applications': applications})


@login_required
def application_detail(request, application_id):
    try:
        application = Application.objects.get(pk=application_id)
        open_engagements = application.engagement_set.filter(status=Engagement.OPEN_STATUS)
        closed_engagements = application.engagement_set.filter(status=Engagement.CLOSED_STATUS)
    except Application.DoesNotExist:
        raise Http404("Application does not exist")

    return render(request, 'tracker/applications/detail.html', {
        'application': application,
        'open_engagements': open_engagements,
        'closed_engagements': closed_engagements
    })


@login_required
def add_application(request):
    form = ApplicationForm(request.POST or None)

    if form.is_valid():
        application = form.save()
        return redirect('tracker:applications.detail', application_id=application.id)

    return render(request, 'tracker/applications/add.html', {'form': form})


@login_required
def edit_application(request, application_id):
    try:
        application = Application.objects.get(pk=application_id)
    except Application.DoesNotExist:
        raise Http404("Application does not exist")

    form = ApplicationForm(request.POST or None, instance=application)

    if request.method == 'POST' and form.is_valid():
            application = form.save()
            return redirect('tracker:applications.detail', application_id=application.id)

    return render(request, 'tracker/applications/edit.html', {'form': form, 'application_id': application_id})
