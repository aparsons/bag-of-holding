import random

from django import forms
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.admin.views.decorators import staff_member_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Count, Q
from django.forms.models import inlineformset_factory
from django.http import Http404
from django.shortcuts import get_object_or_404, render, redirect
from django.views.decorators.http import require_http_methods

from tracker.models import Organization, DataElement, Application, Environment, EnvironmentLocation, EnvironmentCredentials, Engagement, Activity, Tag, Person

from tracker.forms import OrganizationAddForm, OrganizationSettingsGeneralForm, OrganizationDeleteForm
from tracker.forms import ApplicationAddForm, ApplicationDeleteForm, ApplicationSettingsGeneralForm, ApplicationSettingsOrganizationForm, ApplicationSettingsMetadataForm, ApplicationSettingsTagsForm, ApplicationSettingsThreadFixForm
from tracker.forms import ApplicationSettingsDataElementsForm, ApplicationSettingsDCLOverrideForm
from tracker.forms import EnvironmentAddForm, EnvironmentEditForm, EnvironmentDeleteForm, EnvironmentLocationAddForm
from tracker.forms import EngagementAddForm, EngagementEditForm, EngagementDeleteForm, EngagementCommentAddForm
from tracker.forms import ActivityAddForm, ActivityEditForm, ActivityDeleteForm, ActivityCommentAddForm
from tracker.forms import PersonAddForm


# Messages shown on successful actions
action_messages = [
    'Excellent!',
    'Well Done!',
    'Yay!',
    'Choo Choo!',
    'Kudos!',
    'Hey!',
    'Whoa!',
    'Awesome!',
    'Huzzah!',
    ':D',
    'Whack!',
    'Shazzam!',
    'Success!',
    'Alrighty Then!',
    'Thank You!',
    'Nice!',
    'Cheers!',
    'Bam!',
    'Behold!',
    'Good Show!',
    'Boom Chuck!'
]


# Dashboard


@login_required
@require_http_methods(['GET'])
def dashboard_personal(request):
    """The personal dashboard with information relevant to the current user."""

    pending_activities = Activity.objects.filter(users__id=request.user.id).filter(status=Engagement.PENDING_STATUS)
    open_activities = Activity.objects.filter(users__id=request.user.id).filter(status=Engagement.OPEN_STATUS)

    return render(request, 'tracker/dashboard/my_dashboard.html', {
        'pending_activities': pending_activities,
        'open_activities': open_activities,
        'active_tab': 'personal'
    })


@login_required
@require_http_methods(['GET'])
def dashboard_team(request):
    users = User.objects.all()

    open_engagements = Engagement.objects.filter(status=Engagement.OPEN_STATUS)
    pending_engagements = Engagement.objects.filter(status=Engagement.PENDING_STATUS)
    unassigned_activities = Activity.objects.filter(users=None)
    empty_engagements = Engagement.objects.filter(activity__isnull=True)

    return render(request, 'tracker/dashboard/team_dashboard.html', {
        'users': users,
        'open_engagements': open_engagements,
        'pending_engagements': pending_engagements,
        'unassigned_activities': unassigned_activities,
        'empty_engagements': empty_engagements,
        'active_tab': 'team'
    })


@login_required
@require_http_methods(['GET'])
def dashboard_metrics(request):
    # Current Number of Pending/Open/Closed Activities - This week/month/year/alltime
    # Current Number of Pending/Open/Closed Engagements
    # Average Engagement Lengths
    # Average Activity Lengths By Activity


    return render(request, 'tracker/dashboard/metrics.html', {
        'active_tab': 'metrics'
    })


@login_required
@require_http_methods(['GET'])
def dashboard_reports(request):

    return render(request, 'tracker/dashboard/reports.html', {
        'active_tab': 'reports'
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
def organization_overview(request, organization_id):
    organization = get_object_or_404(Organization, pk=organization_id)

    applications = organization.application_set.all()

    return render(request, 'tracker/organizations/overview.html', {
        'organization': organization,
        'applications': applications,
        'active_tab': 'overview'
    })


@login_required
@require_http_methods(['GET'])
def organization_people(request, organization_id):
    organization = get_object_or_404(Organization, pk=organization_id)

    return render(request, 'tracker/organizations/people.html', {
        'organization': organization,
        'active_tab': 'people'
    })


@login_required
@staff_member_required
@require_http_methods(['GET', 'POST'])
def organization_settings_general(request, organization_id):
    organization = get_object_or_404(Organization, pk=organization_id)

    form = OrganizationSettingsGeneralForm(request.POST or None, instance=organization)

    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'You successfully update this organization\'s general information.', extra_tags=random.choice(action_messages))

    return render(request, 'tracker/organizations/settings/general.html', {
        'organization': organization,
        'form': form,
        'active_tab': 'settings',
        'active_side': 'general'
    })


@login_required
@staff_member_required
@require_http_methods(['GET', 'POST'])
def organization_settings_danger(request, organization_id):
    organization = get_object_or_404(Organization, pk=organization_id)

    form = OrganizationDeleteForm(request.POST or None, instance=organization)

    if request.method == 'POST' and form.is_valid():
        organization.delete()
        messages.success(request, 'You successfully deleted the "' + organization.name + '" organization.', extra_tags=random.choice(action_messages))
        return redirect('tracker:dashboard.personal')

    return render(request, 'tracker/organizations/settings/danger.html', {
        'organization': organization,
        'active_tab': 'settings',
        'active_side': 'danger'
    })


@login_required
@staff_member_required
@require_http_methods(['GET', 'POST'])
def organization_add(request):
    form = OrganizationAddForm(request.POST or None)

    if form.is_valid():
        organization = form.save()
        messages.success(request, 'You successfully created this organization.', extra_tags=random.choice(action_messages))
        return redirect('tracker:organization.overview', organization.id)

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
        messages.success(request, 'You successfully created this application.', extra_tags=random.choice(action_messages))
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
                messages.success(request, 'You successfully updated this application\'s general information.', extra_tags=random.choice(action_messages))
        elif 'submit-organization' in request.POST:
            organization_form = ApplicationSettingsOrganizationForm(request.POST, instance=application)
            if organization_form.is_valid():
                organization_form.save()
                messages.success(request, 'You successfully updated this application\'s organization.', extra_tags=random.choice(action_messages))

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

    if 'submit-metadata' in request.POST:
        metadata_form = ApplicationSettingsMetadataForm(request.POST, instance=application)
        if metadata_form.is_valid():
            metadata_form.save()
            messages.success(request, 'You successfully updated this application\'s metadata.', extra_tags=random.choice(action_messages))
    elif 'submit-tags' in request.POST:
        tags_form = ApplicationSettingsTagsForm(request.POST, instance=application)
        if tags_form.is_valid():
            tags_form.save()
            messages.success(request, 'You successfully updated this application\'s tags.', extra_tags=random.choice(action_messages))

    return render(request, 'tracker/applications/settings/metadata.html', {
        'application': application,
        'metadata_form': metadata_form,
        'tags_form': tags_form,
        'active_tab': 'settings',
        'active_side': 'metadata'
    })


@login_required
@require_http_methods(['GET', 'POST'])
def application_settings_data_elements(request, application_id):
    application = get_object_or_404(Application, pk=application_id)

    data_elements_form = ApplicationSettingsDataElementsForm(request.POST or None, instance=application)
    dcl_override_form = ApplicationSettingsDCLOverrideForm(instance=application)

    if request.method == 'POST':
        if data_elements_form.is_valid():
            data_elements_form.save()
            messages.success(request, 'You successfully updated this application\'s data elements.', extra_tags=random.choice(action_messages))
        return redirect('tracker:application.settings.data-elements', application.id)

    return render(request, 'tracker/applications/settings/data_elements.html', {
        'application': application,
        'data_elements_form': data_elements_form,
        'dcl_override_form': dcl_override_form,
        'dcl': application.data_classification_level,
        'dsv': application.data_sensitivity_value,
        'active_tab': 'settings',
        'active_side': 'data_elements'
    })


@login_required
@require_http_methods(['POST'])
def application_settings_data_elements_override(request, application_id):
    application = get_object_or_404(Application, pk=application_id)

    dcl_override_form = ApplicationSettingsDCLOverrideForm(request.POST or None, instance=application)

    if dcl_override_form.is_valid():
        dcl_override_form.save()
        messages.success(request, 'This application\'s data classification override has been updated.', extra_tags=random.choice(action_messages))

    return redirect('tracker:application.settings.data-elements', application.id)


@login_required
@require_http_methods(['GET', 'POST'])
def application_settings_services(request, application_id):
    application = get_object_or_404(Application, pk=application_id)

    threadfix_form = ApplicationSettingsThreadFixForm(instance=application)

    if 'submit-threadfix' in request.POST:
        threadfix_form = ApplicationSettingsThreadFixForm(request.POST, instance=application)
        if threadfix_form.is_valid():
            threadfix_form.save()
            messages.success(request, 'You successfully updated this application\'s ThreadFix information.', extra_tags=random.choice(action_messages))

    return render(request, 'tracker/applications/settings/services.html', {
        'application': application,
        'threadfix_form': threadfix_form,
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
        messages.success(request, 'You successfully deleted the "' + application.name + '" application.', extra_tags=random.choice(action_messages))
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
        messages.success(request, 'You successfully created this environment.', extra_tags=random.choice(action_messages))
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
        messages.success(request, 'You successfully updated this environment.', extra_tags=random.choice(action_messages))
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
        messages.success(request, 'You successfully updated these locations.', extra_tags=random.choice(action_messages))
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
        messages.success(request, 'You successfully updated these credentials.', extra_tags=random.choice(action_messages))
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
        messages.success(request, 'You successfully deleted the "' + environment.get_environment_type_display() + '" application.', extra_tags=random.choice(action_messages))
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
        messages.success(request, 'You successfully created this environment location.', extra_tags=random.choice(action_messages))
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
        messages.success(request, 'You successfully created this engagement.', extra_tags=random.choice(action_messages))
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
        messages.success(request, 'You successfully updated this engagement.', extra_tags=random.choice(action_messages))
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
        messages.success(request, 'You successfully added a comment to this engagement.', extra_tags=random.choice(action_messages))

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
        messages.success(request, 'You successfully added this activity.', extra_tags=random.choice(action_messages))
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
        messages.success(request, 'You successfully updated this activity.', extra_tags=random.choice(action_messages))
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
        messages.success(request, 'You successfully deleted the activity.', extra_tags=random.choice(action_messages))
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
        messages.success(request, 'You successfully added a comment to this activity.', extra_tags=random.choice(action_messages))

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
        messages.success(request, 'You successfully created this person.', extra_tags=random.choice(action_messages))
        return redirect('tracker:people.list')

    return render(request, 'tracker/people/add.html', {'form': form})


@login_required
@require_http_methods(['GET'])
def people_detail(request, person_id):
    person = get_object_or_404(Person, pk=person_id)

    return render(request, 'tracker/people/detail.html', {
        'person': person
    })
