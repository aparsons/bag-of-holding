from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Count
from django.http import Http404
from django.shortcuts import render, redirect

from tracker.models import Application, Engagement, Activity, Tag
from tracker.forms import ApplicationForm

# Create your views here.

@login_required
def application_list(request):
    application_list = Application.objects.all()
    tags = Tag.objects.all().annotate(total_applications=Count('application')).order_by('-total_applications', 'name')

    paginator = Paginator(application_list, 20)

    page = request.GET.get('page')
    try:
        applications = paginator.page(page)
    except PageNotAnInteger:
        applications = paginator.page(1)
    except EmptyPage:
        applications = paginator.page(paginator.num_pages)

    return render(request, 'tracker/applications/list.html', {'applications': applications, 'tags': tags})


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
def application_add(request):
    form = ApplicationForm(request.POST or None)

    if form.is_valid():
        application = form.save()
        return redirect('tracker:application.detail', application_id=application.id)

    return render(request, 'tracker/applications/add.html', {'form': form})


@login_required
def application_edit(request, application_id):
    try:
        application = Application.objects.get(pk=application_id)
    except Application.DoesNotExist:
        raise Http404("Application does not exist")

    form = ApplicationForm(request.POST or None, instance=application)

    if request.method == 'POST' and form.is_valid():
            application = form.save()
            return redirect('tracker:application.detail', application_id=application.id)

    return render(request, 'tracker/applications/edit.html', {'form': form, 'application_id': application_id})


@login_required
def application_delete(request, application_id):
    try:
        application = Application.objects.get(pk=application_id)
    except Application.DoesNotExist:
        raise Http404("Application does not exist")

    application.delete()

    return redirect('tracker:applications.list')


@login_required
def engagement_add(request, application_id):
    try:
        application = Application.objects.get(pk=application_id)
    except Application.DoesNotExist:
        raise Http404("Application does not exist")

    return render(request, 'tracker/engagements/add.html')


@login_required
def engagement_detail(request, engagement_id):
    try:
        engagement = Engagement.objects.get(pk=engagement_id)
        open_activities = engagement.activity_set.filter(status=Activity.OPEN_STATUS)
    except Engagement.DoesNotExist:
        raise Http404("Engagement does not exist")

    return render(request, 'tracker/engagements/detail.html', {'engagement': engagement, 'open_activities': open_activities})
