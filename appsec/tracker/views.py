from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Count
from django.http import Http404
from django.shortcuts import get_object_or_404, render, redirect
from django.views.decorators.http import require_http_methods

from tracker.models import Application, Engagement, Activity, Tag, Person
from tracker.forms import ApplicationAddForm, ApplicationEditForm, ApplicationDeleteForm, EngagementAddForm, EngagementEditForm, EngagementDeleteForm, EngagementCommentAddForm, ActivityAddForm, ActivityEditForm, ActivityDeleteForm, ActivityCommentAddForm


# Dashboard


@login_required
@require_http_methods(['GET'])
def dashboard_detail(request):

    activities = Activity.objects.filter(users__id=request.user.id)

    return render(request, 'tracker/dashboard.html', {
        'activities': activities
    })


# Application


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
        messages.success(request, 'You successfully created this application.', extra_tags='Well done!')
        return redirect('tracker:application.detail', application_id=application.id)

    return render(request, 'tracker/applications/add.html', {'form': form})


@login_required
@require_http_methods(['GET', 'POST'])
def application_edit(request, application_id):
    application = get_object_or_404(Application, pk=application_id)

    form = ApplicationEditForm(request.POST or None, instance=application)

    if request.method == 'POST' and form.is_valid():
        application = form.save()
        messages.success(request, 'You successfully updated this application.', extra_tags='Yay!')
        return redirect('tracker:application.detail', application_id=application.id)

    return render(request, 'tracker/applications/edit.html', {'form': form, 'application': application})


@login_required
@require_http_methods(['POST'])
def application_delete(request, application_id):
    application = get_object_or_404(Application, pk=application_id)

    form = ApplicationDeleteForm(request.POST or None)

    if form.is_valid():
        application.delete()
        messages.success(request, 'You successfully deleted the "' + application.name + '" application.', extra_tags='Hey!')
        return redirect('tracker:application.list')
    else:
        return redirect('tracker:applications.detail', application.id)


# Engagement


@login_required
@require_http_methods(['GET'])
def engagement_detail(request, engagement_id):
    engagement = get_object_or_404(Engagement, pk=engagement_id)

    pending_activities = engagement.activity_set.filter(status=Activity.PENDING_STATUS)
    open_activities = engagement.activity_set.filter(status=Activity.OPEN_STATUS)
    closed_activities = engagement.activity_set.filter(status=Activity.CLOSED_STATUS)

    comments = engagement.engagementcomment_set.all()

    form = EngagementCommentAddForm()

    return render(request, 'tracker/engagements/detail.html', {
        'engagement': engagement,
        'pending_activities': pending_activities,
        'open_activities': open_activities,
        'closed_activities': closed_activities,
        'comments': comments,
        'form': form
    })


@login_required
@require_http_methods(['GET', 'POST'])
def engagement_add(request, application_id):
    application = get_object_or_404(Application, pk=application_id)

    form = EngagementAddForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        engagement = form.save(commit=False)
        engagement.application = application
        engagement.save()
        messages.success(request, 'You successfully created this engagement.', extra_tags='Alrighty!')
        return redirect('tracker:engagement.detail', engagement_id=engagement.id)
    else:
        return render(request, 'tracker/engagements/add.html', {'form': form, 'application': application})


@login_required
@require_http_methods(['GET', 'POST'])
def engagement_edit(request, engagement_id):
    engagement = get_object_or_404(Engagement, pk=engagement_id)

    form = EngagementEditForm(request.POST or None, instance=engagement)

    if request.method == 'POST' and form.is_valid():
        engagement = form.save()
        messages.success(request, 'You successfully updated this engagement.', extra_tags='Success!')
        return redirect('tracker:engagement.detail', engagement_id=engagement.id)

    return render(request, 'tracker/engagements/edit.html', {'form': form, 'engagement': engagement})


@login_required
@require_http_methods(['POST'])
def engagement_delete(request, engagement_id):
    engagement = get_object_or_404(Engagement, pk=engagement_id)

    form = EngagementDeleteForm(request.POST or None)

    if form.is_valid():
        engagement.delete()
        messages.success(request, 'You successfully deleted the engagement.', extra_tags='Boom!')
        return redirect('tracker:application.detail', engagement.application.id)
    else:
        return redirect('tracker:engagement.detail', engagement.id)


@login_required
@require_http_methods(['POST'])
def engagement_comment_add(request, engagement_id):
    engagement = get_object_or_404(Engagement, pk=engagement_id)

    form = EngagementCommentAddForm(request.POST)

    if form.is_valid():
        comment = form.save(commit=False)
        comment.engagement = engagement
        comment.user = request.user
        comment.save()
        messages.success(request, 'You successfully added a comment to this engagement.', extra_tags='Thank you!')

    return redirect('tracker:engagement.detail', engagement_id=engagement.id)


# Activity


@login_required
@require_http_methods(['GET'])
def activity_detail(request, activity_id):
    activity = get_object_or_404(Activity, pk=activity_id)

    comments = activity.activitycomment_set.all()

    form = ActivityCommentAddForm()

    return render(request, 'tracker/activities/detail.html', {
        'activity': activity,
        'comments': comments,
        'form': form
    })


@login_required
@require_http_methods(['GET', 'POST'])
def activity_add(request, engagement_id):
    engagement = get_object_or_404(Engagement, pk=engagement_id)

    form = ActivityAddForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        activity = form.save(commit=False)
        activity.engagement = engagement
        activity.save()
        form.save_m2m() # https://docs.djangoproject.com/en/1.7/topics/forms/modelforms/#the-save-method
        messages.success(request, 'You successfully added this activity.', extra_tags='Nice!')
        return redirect('tracker:activity.detail', activity_id=activity.id)
    else:
        return render(request, 'tracker/activities/add.html', {'form': form, 'engagement': engagement})


@login_required
@require_http_methods(['GET', 'POST'])
def activity_edit(request, activity_id):
    activity = get_object_or_404(Activity, pk=activity_id)

    form = ActivityEditForm(request.POST or None, instance=activity)

    if request.method == 'POST' and form.is_valid():
        activity = form.save()
        messages.success(request, 'You successfully updated this activity.', extra_tags='Cheers!')
        return redirect('tracker:activity.detail', activity_id=activity.id)

    return render(request, 'tracker/activities/edit.html', {'form': form, 'activity': activity})


@login_required
@require_http_methods(['POST'])
def activity_delete(request, activity_id):
    activity = get_object_or_404(Activity, pk=activity_id)

    form = ActivityDeleteForm(request.POST or None)

    if form.is_valid():
        activity.delete()
        messages.success(request, 'You successfully deleted the activity.', extra_tags='Bam!')
        return redirect('tracker:engagement.detail', activity.engagement.id)
    else:
        return redirect('tracker:activity.detail', activity.id)


@login_required
@require_http_methods(['POST'])
def activity_comment_add(request, activity_id):
    activity = get_object_or_404(Activity, pk=activity_id)

    form = ActivityCommentAddForm(request.POST)

    if form.is_valid():
        comment = form.save(commit=False)
        comment.activity = activity
        comment.user = request.user
        comment.save()
        messages.success(request, 'You successfully added a comment to this activity.', extra_tags='Behold!')

    return redirect('tracker:activity.detail', activity_id=activity.id)


# People


@login_required
@require_http_methods(['GET'])
def people_list(request):
    person_list = Person.objects.all()

    paginator = Paginator(person_list, 5)

    page = request.GET.get('page')
    try:
        people = paginator.page(page)
    except PageNotAnInteger:
        people = paginator.page(1)
    except EmptyPage:
        people = paginator.page(paginator.num_pages)

    return render(request, 'tracker/people/list.html', {'people': people})
