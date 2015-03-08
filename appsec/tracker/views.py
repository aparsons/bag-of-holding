from django import forms
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Count
from django.forms.models import inlineformset_factory
from django.http import Http404
from django.shortcuts import get_object_or_404, render, redirect
from django.views.decorators.http import require_http_methods

from tracker.models import Organization, Application, Environment, EnvironmentLocation, EnvironmentCredentials, Engagement, Activity, Tag, Person

from tracker.forms import OrganizationAddForm
from tracker.forms import ApplicationAddForm, ApplicationDeleteForm, ApplicationSettingsGeneralForm, ApplicationSettingsOrganizationForm, ApplicationSettingsMetadataForm, ApplicationSettingsTagsForm
from tracker.forms import EnvironmentAddForm, EnvironmentEditForm, EnvironmentDeleteForm, EnvironmentLocationAddForm
from tracker.forms import EngagementAddForm, EngagementEditForm, EngagementDeleteForm, EngagementCommentAddForm
from tracker.forms import ActivityAddForm, ActivityEditForm, ActivityDeleteForm, ActivityCommentAddForm
from tracker.forms import PersonAddForm


# Dashboard


@login_required
@require_http_methods(['GET'])
def dashboard_detail(request):

    activities = Activity.objects.filter(users__id=request.user.id)

    return render(request, 'tracker/dashboard.html', {
        'activities': activities
    })


# Management


@login_required
@staff_member_required
@require_http_methods(['GET'])
def management_services(request):

    return render(request, 'tracker/management/services.html', {
        'active': 'services'
    })


@login_required
@staff_member_required
@require_http_methods(['GET'])
def management_users(request):

    return render(request, 'tracker/management/users.html', {
        'active': 'users'
    })


# Organization


@login_required
@require_http_methods(['GET'])
def organization_detail(request, organization_id):
    organization = get_object_or_404(Organization, pk=organization_id)

    applications = organization.application_set.all()

    return render(request, 'tracker/organizations/detail.html', {
        'organization': organization,
        'applications': applications
    })


@login_required
@require_http_methods(['GET', 'POST'])
def organization_add(request):
    form = OrganizationAddForm(request.POST or None)

    if form.is_valid():
        organization = form.save()
        messages.success(request, 'You successfully created this organization.', extra_tags='Excellent!')
        return redirect('tracker:application.list')

    return render(request, 'tracker/organizations/add.html', {
        'form': form
    })


# Application


@login_required
@require_http_methods(['GET'])
def application_list(request):
    queries = request.GET.copy()
    if queries.__contains__('page'):
        del queries['page']

    application_list = Application.objects.all()

    tag_id = request.GET.get('tag', 0)
    if tag_id:
        application_list = application_list.filter(tags__id=tag_id)

    tags = Tag.objects.all().annotate(total_applications=Count('application')).order_by('-total_applications', 'name')

    paginator = Paginator(application_list, 20)

    page = request.GET.get('page')
    try:
        applications = paginator.page(page)
    except PageNotAnInteger:
        applications = paginator.page(1)
    except EmptyPage:
        applications = paginator.page(paginator.num_pages)

    return render(request, 'tracker/applications/list.html', {
        'applications': applications,
        'tags': tags,
        'queries': queries,
        'active_filter_tag': int(tag_id)
    })


@login_required
@require_http_methods(['GET'])
def application_overview(request, application_id):
    application = get_object_or_404(Application, pk=application_id)

    return render(request, 'tracker/applications/overview.html', {
        'application': application,
        'active_tab': 'overview'
    })


@login_required
@require_http_methods(['GET'])
def application_engagements(request, application_id):
    application = get_object_or_404(Application, pk=application_id)

    pending_engagements = application.engagement_set.filter(status=Engagement.PENDING_STATUS)
    open_engagements = application.engagement_set.filter(status=Engagement.OPEN_STATUS)
    closed_engagements = application.engagement_set.filter(status=Engagement.CLOSED_STATUS)

    return render(request, 'tracker/applications/engagements.html', {
        'application': application,
        'pending_engagements': pending_engagements,
        'open_engagements': open_engagements,
        'closed_engagements': closed_engagements,
        'active_tab': 'engagements'
    })


@login_required
@require_http_methods(['GET'])
def application_environments(request, application_id):
    application = get_object_or_404(Application, pk=application_id)

    return render(request, 'tracker/applications/environments.html', {
        'application': application,
        'active_tab': 'environments'
    })


@login_required
@require_http_methods(['GET'])
def application_people(request, application_id):
    application = get_object_or_404(Application, pk=application_id)

    return render(request, 'tracker/applications/people.html', {
        'application': application,
        'active_tab': 'people'
    })


@login_required
@require_http_methods(['GET', 'POST'])
def application_add(request):
    form = ApplicationAddForm(request.POST or None)

    if form.is_valid():
        application = form.save()
        messages.success(request, 'You successfully created this application.', extra_tags='Well done!')
        return redirect('tracker:application.overview', application_id=application.id)

    return render(request, 'tracker/applications/add.html', {
        'form': form
    })


@login_required
@require_http_methods(['GET', 'POST'])
def application_settings_general(request, application_id):
    application = get_object_or_404(Application, pk=application_id)

    general_form = ApplicationSettingsGeneralForm(instance=application)
    organization_form = ApplicationSettingsOrganizationForm(instance=application)

    if request.method == 'POST':
        if 'submit-general' in request.POST:
            general_form = ApplicationSettingsGeneralForm(request.POST, instance=application)
            if general_form.is_valid():
                general_form.save()
                messages.success(request, 'You successfully updated this application\'s general information.', extra_tags='Yay!')
        elif 'submit-organization' in request.POST:
            organization_form = ApplicationSettingsOrganizationForm(request.POST, instance=application)
            if organization_form.is_valid():
                organization_form.save()
                messages.success(request, 'You successfully updated this application\'s organization.', extra_tags='Choo Choo!')

    return render(request, 'tracker/applications/settings/general.html', {
        'application': application,
        'general_form': general_form,
        'organization_form': organization_form,
        'active_tab': 'settings',
        'active_side': 'general'
    })


@login_required
@require_http_methods(['GET', 'POST'])
def application_settings_metadata(request, application_id):
    application = get_object_or_404(Application, pk=application_id)

    metadata_form = ApplicationSettingsMetadataForm(instance=application)
    tags_form = ApplicationSettingsTagsForm(instance=application)

    if request.method == 'POST':
        if 'submit-metadata' in request.POST:
            metadata_form = ApplicationSettingsMetadataForm(request.POST, instance=application)
            if metadata_form.is_valid():
                metadata_form.save()
                messages.success(request, 'You successfully updated this application\'s metadata.', extra_tags='Yay!')
        elif 'submit-tags' in request.POST:
            tags_form = ApplicationSettingsTagsForm(request.POST, instance=application)
            if tags_form.is_valid():
                tags_form.save()
                messages.success(request, 'You successfully updated this application\'s tags.', extra_tags='Yay!')

    return render(request, 'tracker/applications/settings/metadata.html', {
        'application': application,
        'metadata_form': metadata_form,
        'tags_form': tags_form,
        'active_tab': 'settings',
        'active_side': 'metadata'
    })


@login_required
@require_http_methods(['GET', 'POST'])
def application_settings_services(request, application_id):
    application = get_object_or_404(Application, pk=application_id)

    return render(request, 'tracker/applications/settings/services.html', {
        'application': application,
        'active_tab': 'settings',
        'active_side': 'services'
    })


@login_required
@require_http_methods(['GET'])
def application_settings_danger(request, application_id):
    application = get_object_or_404(Application, pk=application_id)

    return render(request, 'tracker/applications/settings/danger.html', {
        'application': application,
        'active_tab': 'settings',
        'active_side': 'danger'
    })


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


# Environment


@login_required
@require_http_methods(['GET', 'POST'])
def environment_add(request, application_id):
    application = get_object_or_404(Application, pk=application_id)

    form = EnvironmentAddForm(request.POST or None)

    if form.is_valid():
        environment = form.save(commit=False)
        environment.application = application
        environment.save()
        messages.success(request, 'You successfully created this environment.', extra_tags='Woah!')
        return redirect('tracker:application.environments', application_id=application.id)

    return render(request, 'tracker/environments/add.html', {
        'application': application,
        'form': form,
        'active_tab': 'environments'
    })


@login_required
@require_http_methods(['GET', 'POST'])
def environment_edit_general(request, environment_id):
    environment = get_object_or_404(Environment, pk=environment_id)

    form = EnvironmentEditForm(request.POST or None, instance=environment)

    if form.is_valid():
        environment = form.save()
        messages.success(request, 'You successfully updated this environment.', extra_tags='Awesome!')
        return redirect('tracker:environment.edit.general', environment_id=environment.id)

    return render(request, 'tracker/environments/edit/general.html', {
        'application': environment.application,
        'environment': environment,
        'form': form,
        'active_tab': 'environments',
        'active_side': 'general'
    })


@login_required
@require_http_methods(['GET', 'POST'])
def environment_edit_locations(request, environment_id):
    environment = get_object_or_404(Environment, pk=environment_id)

    EnvironmentLocationInlineFormSet = inlineformset_factory(Environment, EnvironmentLocation, extra=1,
        widgets = {
            'notes': forms.Textarea(attrs = {'rows': 2})
        }
    )

    formset = EnvironmentLocationInlineFormSet(request.POST or None, instance=environment)

    if formset.is_valid():
        formset.save()
        messages.success(request, 'You successfully updated these locations.', extra_tags='Huzzah!')
        return redirect('tracker:environment.edit.locations', environment_id=environment.id)

    return render(request, 'tracker/environments/edit/locations.html', {
        'application': environment.application,
        'environment': environment,
        'formset': formset,
        'active_tab': 'environments',
        'active_side': 'locations'
    })


@login_required
@require_http_methods(['GET', 'POST'])
def environment_edit_credentials(request, environment_id):
    environment = get_object_or_404(Environment, pk=environment_id)

    EnvironmentCredentialsInlineFormSet = inlineformset_factory(Environment, EnvironmentCredentials, extra=1,
        widgets = {
            'notes': forms.Textarea(attrs = {'rows': 2})
        }
    )

    formset = EnvironmentCredentialsInlineFormSet(request.POST or None, instance=environment)

    if formset.is_valid():
        formset.save()
        messages.success(request, 'You successfully updated these credentials.', extra_tags=':D')
        return redirect('tracker:environment.edit.credentials', environment_id=environment.id)

    return render(request, 'tracker/environments/edit/credentials.html', {
        'application': environment.application,
        'environment': environment,
        'formset': formset,
        'active_tab': 'environments',
        'active_side': 'credentials'
    })


@login_required
@require_http_methods(['GET'])
def environment_edit_danger(request, environment_id):
    environment = get_object_or_404(Environment, pk=environment_id)

    return render(request, 'tracker/environments/edit/danger.html', {
        'application': environment.application,
        'environment': environment,
        'active_tab': 'environments',
        'active_side': 'danger'
    })


@login_required
@require_http_methods(['POST'])
def environment_delete(request, environment_id):
    environment = get_object_or_404(Environment, pk=environment_id)

    form = EnvironmentDeleteForm(request.POST or None)

    if form.is_valid():
        environment.delete()
        messages.success(request, 'You successfully deleted the "' + environment.get_environment_type_display() + '" application.', extra_tags='Whack!')
        return redirect('tracker:application.environments', environment.application.id)
    else:
        return redirect('tracker:environment.edit.danger', environment.id)


@login_required
@require_http_methods(['GET', 'POST'])
def environment_location_add(request, environment_id):
    environment = get_object_or_404(Environment, pk=environment_id)

    form = EnvironmentLocationAddForm(request.POST or None)

    if form.is_valid():
        environment_location = form.save(commit=False)
        environment_location.environment = environment
        environment_location.save()
        messages.success(request, 'You successfully created this environment location.', extra_tags='Shazzam!')
        return redirect('tracker:environment.detail', environment_id=environment.id)

    return render(request, 'tracker/environments/locations/add.html', {
        'form': form,
        'environment': environment
    })


# Engagement


@login_required
@require_http_methods(['GET'])
def engagement_detail(request, engagement_id):
    engagement = get_object_or_404(Engagement, pk=engagement_id)

    pending_activities = engagement.activity_set.filter(status=Activity.PENDING_STATUS)
    open_activities = engagement.activity_set.filter(status=Activity.OPEN_STATUS)
    closed_activities = engagement.activity_set.filter(status=Activity.CLOSED_STATUS)

    form = EngagementCommentAddForm()

    return render(request, 'tracker/engagements/detail.html', {
        'application': engagement.application,
        'engagement': engagement,
        'pending_activities': pending_activities,
        'open_activities': open_activities,
        'closed_activities': closed_activities,
        'form': form,
        'active_tab': 'engagements'
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
        return render(request, 'tracker/engagements/add.html', {
            'application': application,
            'form': form,
            'active_tab': 'engagements'
        })


@login_required
@require_http_methods(['GET', 'POST'])
def engagement_edit(request, engagement_id):
    engagement = get_object_or_404(Engagement, pk=engagement_id)

    form = EngagementEditForm(request.POST or None, instance=engagement)

    if request.method == 'POST' and form.is_valid():
        engagement = form.save()
        messages.success(request, 'You successfully updated this engagement.', extra_tags='Success!')
        return redirect('tracker:engagement.detail', engagement_id=engagement.id)

    return render(request, 'tracker/engagements/edit.html', {
        'application': engagement.application,
        'engagement': engagement,
        'form': form,
        'active_tab': 'engagements'
    })


@login_required
@require_http_methods(['POST'])
def engagement_delete(request, engagement_id):
    engagement = get_object_or_404(Engagement, pk=engagement_id)

    form = EngagementDeleteForm(request.POST or None)

    if form.is_valid():
        engagement.delete()
        messages.success(request, 'You successfully deleted the engagement.', extra_tags='Boom!')
        return redirect('tracker:application.overview', engagement.application.id)
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

    form = ActivityCommentAddForm()

    return render(request, 'tracker/activities/detail.html', {
        'application': activity.engagement.application,
        'activity': activity,
        'form': form,
        'active_tab': 'engagements'
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
        return render(request, 'tracker/activities/add.html', {
            'application': engagement.application,
            'engagement': engagement,
            'form': form,
            'active_tab': 'engagements'
        })


@login_required
@require_http_methods(['GET', 'POST'])
def activity_edit(request, activity_id):
    activity = get_object_or_404(Activity, pk=activity_id)

    form = ActivityEditForm(request.POST or None, instance=activity)

    if request.method == 'POST' and form.is_valid():
        activity = form.save()
        messages.success(request, 'You successfully updated this activity.', extra_tags='Cheers!')
        return redirect('tracker:activity.detail', activity_id=activity.id)

    return render(request, 'tracker/activities/edit.html', {
        'application': activity.engagement.application,
        'activity': activity,
        'form': form,
        'active_tab': 'engagements'
    })


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


@login_required
@require_http_methods(['GET', 'POST'])
def people_add(request):
    form = PersonAddForm(request.POST or None)

    if form.is_valid():
        person = form.save()
        messages.success(request, 'You successfully created this person.', extra_tags='Good show!')
        return redirect('tracker:people.list')

    return render(request, 'tracker/people/add.html', {'form': form})


@login_required
@require_http_methods(['GET'])
def people_detail(request, person_id):
    person = get_object_or_404(Person, pk=person_id)

    return render(request, 'tracker/people/detail.html', {
        'person': person
    })
