from django.contrib.auth.decorators import login_required
from django.contrib.messages import info, warning, error
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Count
from django.http import Http404
from django.shortcuts import get_object_or_404, render, redirect
from django.views.decorators.http import require_http_methods

from tracker.models import Application, Engagement, Activity, Tag
from tracker.forms import ApplicationAddForm, ApplicationEditForm, ApplicationDeleteForm, EngagementAddForm

# Create your views here.

@login_required
@require_http_methods(['GET'])
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
@require_http_methods(['GET'])
def application_detail(request, application_id):
    application = get_object_or_404(Application, pk=application_id)

    pending_engagements = application.engagement_set.filter(status=Engagement.PENDING_STATUS)
    open_engagements = application.engagement_set.filter(status=Engagement.OPEN_STATUS)
    closed_engagements = application.engagement_set.filter(status=Engagement.CLOSED_STATUS)

    return render(request, 'tracker/applications/detail.html', {
        'application': application,
        'pending_engagements': pending_engagements,
        'open_engagements': open_engagements,
        'closed_engagements': closed_engagements
    })


@login_required
@require_http_methods(['GET', 'POST'])
def application_add(request):
    form = ApplicationAddForm(request.POST or None)

    if form.is_valid():
        application = form.save()
        return redirect('tracker:application.detail', application_id=application.id)

    return render(request, 'tracker/applications/add.html', {'form': form})


@login_required
@require_http_methods(['GET', 'POST'])
def application_edit(request, application_id):
    application = get_object_or_404(Application, pk=application_id)

    form = ApplicationEditForm(request.POST or None, instance=application)
    
    if request.method == 'POST' and form.is_valid():
        application = form.save()
        return redirect('tracker:application.detail', application_id=application.id)

    return render(request, 'tracker/applications/edit.html', {'form': form, 'application': application})


@login_required
@require_http_methods(['POST'])
def application_delete(request, application_id):
    application = get_object_or_404(Application, pk=application_id)

    form = ApplicationDeleteForm(request.POST or None)

    if form.is_valid():
        application.delete()
        return redirect('tracker:application.list')
    else:
        return redirect('tracker:applications.detail', application.id)


@login_required
@require_http_methods(['GET', 'POST'])
def engagement_add(request, application_id):
    application = get_object_or_404(Application, pk=application_id)

    form = EngagementAddForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        engagement = form.save(commit=False)
        engagement.application = application
        engagement.save()
        return redirect('tracker:engagement.detail', engagement_id=engagement.id)
    else:
        return render(request, 'tracker/engagements/add.html', {'form': form, 'application': application})


@login_required
@require_http_methods(['GET'])
def engagement_detail(request, engagement_id):
    engagement = get_object_or_404(Engagement, pk=engagement_id)

    pending_activities = engagement.activity_set.filter(status=Activity.PENDING_STATUS)
    open_activities = engagement.activity_set.filter(status=Activity.OPEN_STATUS)
    closed_activities = engagement.activity_set.filter(status=Activity.CLOSED_STATUS)

    return render(request, 'tracker/engagements/detail.html', {
        'engagement': engagement,
        'pending_activities': pending_activities,
        'open_activities': open_activities,
        'closed_activities': closed_activities
    })

@login_required
@require_http_methods(['GET'])
def activity_detail(request, activity_id):
    return render(request, 'tracker/activities/detail.html')
