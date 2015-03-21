import random

from django import forms
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordChangeForm, UserChangeForm
from django.contrib.admin.views.decorators import staff_member_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Count, Q, Sum
from django.forms.models import inlineformset_factory
from django.http import Http404
from django.shortcuts import get_object_or_404, render, redirect
from django.views.decorators.http import require_http_methods

from boh.models import Organization, DataElement, Application, Environment, EnvironmentLocation, EnvironmentCredentials, Engagement, Activity, Tag, Person, ThreadFix
from boh.forms import UserProfileForm
from boh.forms import OrganizationAddForm, OrganizationSettingsGeneralForm, OrganizationDeleteForm
from boh.forms import ApplicationAddForm, ApplicationDeleteForm, ApplicationSettingsGeneralForm, ApplicationSettingsOrganizationForm, ApplicationSettingsMetadataForm, ApplicationSettingsTagsForm, ApplicationSettingsThreadFixForm
from boh.forms import ApplicationSettingsDataElementsForm, ApplicationSettingsDCLOverrideForm
from boh.forms import EnvironmentAddForm, EnvironmentEditForm, EnvironmentDeleteForm, EnvironmentLocationAddForm
from boh.forms import EngagementAddForm, EngagementEditForm, EngagementStatusForm, EngagementDeleteForm, EngagementCommentAddForm
from boh.forms import ActivityAddForm, ActivityEditForm, ActivityStatusForm, ActivityDeleteForm, ActivityCommentAddForm
from boh.forms import PersonForm, PersonDeleteForm
from boh.forms import ThreadFixForm, ThreadFixDeleteForm


# Messages shown on successful actions
success_messages = [
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
    'Boom Chuck!',
    'Bingo!'
]

error_messages = [
    'Uh Oh!',
    'Whoops!',
    'Oopsie!',
    'Rats!',
    'Darn!',
    'Crud!',
    'Yikes!'
]


# Dashboard


@login_required
@require_http_methods(['GET'])
def dashboard_personal(request):
    """The personal dashboard with information relevant to the current user."""

    pending_activities = Activity.objects.filter(users__id=request.user.id).filter(status=Engagement.PENDING_STATUS)
    open_activities = Activity.objects.filter(users__id=request.user.id).filter(status=Engagement.OPEN_STATUS)

    return render(request, 'boh/dashboard/my_dashboard.html', {
        'pending_activities': pending_activities,
        'open_activities': open_activities,
        'active_top': 'dashboard',
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

    return render(request, 'boh/dashboard/team_dashboard.html', {
        'users': users,
        'open_engagements': open_engagements,
        'pending_engagements': pending_engagements,
        'unassigned_activities': unassigned_activities,
        'empty_engagements': empty_engagements,
        'active_top': 'dashboard',
        'active_tab': 'team'
    })


@login_required
@require_http_methods(['GET'])
def dashboard_metrics(request):

    # Current Number of Pending/Open/Closed Activities - This week/month/year/alltime
    # Current Number of Pending/Open/Closed Engagements
    # Average Engagement Lengths
    # Average Activity Lengths By Activity

    return render(request, 'boh/dashboard/metrics.html', {
        'active_top': 'dashboard',
        'active_tab': 'metrics'
    })


@login_required
@require_http_methods(['GET'])
def dashboard_reports(request):

    # BISO Reports
    # Top 10 Reports

    return render(request, 'boh/dashboard/reports.html', {
        'active_top': 'dashboard',
        'active_tab': 'reports'
    })


# Management


@login_required
@staff_member_required
@require_http_methods(['GET'])
def management_services(request):

    threadfix_services = ThreadFix.objects.all()

    return render(request, 'boh/management/services.html', {
        'threadfix_services': threadfix_services,
        'active_top': 'management',
        'active': 'services'
    })


@login_required
@staff_member_required
@require_http_methods(['GET', 'POST'])
def management_services_threadfix_add(request):
    threadfix_form = ThreadFixForm(request.POST or None)

    if request.method == 'POST':
        if threadfix_form.is_valid():
            threadfix = threadfix_form.save()
            messages.success(request, 'You successfully created the "' + threadfix.name + '" ThreadFix service.', extra_tags=random.choice(success_messages))
            return redirect('boh:management.services')
        else:
            messages.error(request, 'There was a problem creating this ThreadFix service.', extra_tags=random.choice(error_messages))

    return render(request, 'boh/management/threadfix/add.html', {
        'threadfix_form': threadfix_form,
        'active_top': 'management',
        'active': 'services'
    })


@login_required
@staff_member_required
@require_http_methods(['GET', 'POST'])
def management_services_threadfix_edit(request, threadfix_id):
    threadfix = get_object_or_404(ThreadFix, pk=threadfix_id)

    threadfix_form = ThreadFixForm(request.POST or None, instance=threadfix)

    if request.method == 'POST':
        if threadfix_form.is_valid():
            threadfix = threadfix_form.save()
            messages.success(request, 'You successfully updated the "' + threadfix.name + '" ThreadFix service.', extra_tags=random.choice(success_messages))
            return redirect('boh:management.services')
        else:
            messages.error(request, 'There was a problem updating this ThreadFix service.', extra_tags=random.choice(error_messages))

    return render(request, 'boh/management/threadfix/edit.html', {
        'threadfix': threadfix,
        'threadfix_form': threadfix_form,
        'active_top': 'management',
        'active': 'services'
    })


@login_required
@staff_member_required
@require_http_methods(['POST'])
def management_services_threadfix_delete(request, threadfix_id):
    threadfix = get_object_or_404(ThreadFix, pk=threadfix_id)

    form = ThreadFixDeleteForm(request.POST, instance=threadfix)

    if form.is_valid():
        threadfix.delete()
        messages.success(request, 'You successfully deleted the "' + threadfix.name + '" ThreadFix service.', extra_tags=random.choice(success_messages))
        return redirect('boh:management.services')
    else:
        messages.error(request, 'There was a problem deleting this ThreadFix service.', extra_tags=random.choice(error_messages))
        return redirect('boh:management.services.threadfix.edit', threadfix.id)


@login_required
@staff_member_required
@require_http_methods(['GET'])
def management_users(request):

    return render(request, 'boh/management/users.html', {
        'active_top': 'management',
        'active': 'users'
    })


# User


@login_required
@require_http_methods(['GET', 'POST'])
def user_profile(request):
    profile_form = UserProfileForm(request.POST or None, instance=request.user)

    if request.method == 'POST':
        if profile_form.is_valid():
            profile_form.save()
            messages.success(request, 'You successfully updated your profile.', extra_tags=random.choice(success_messages))
        else:
            messages.error(request, 'There was a problem updating your profile.', extra_tags=random.choice(error_messages))

    return render(request, 'boh/user/profile.html', {
        'profile_form': profile_form,
        'active_top': 'user',
        'active_side': 'profile'
    })


@login_required
@require_http_methods(['GET', 'POST'])
def user_change_password(request):
    password_form = PasswordChangeForm(user=request.user, data=request.POST or None)

    if request.method == 'POST':
        if password_form.is_valid():
            password_form.save()
            update_session_auth_hash(request, password_form.user)
            messages.success(request, 'You successfully changed your password.', extra_tags=random.choice(success_messages))
        else:
            messages.error(request, 'There was a problem changing your password.', extra_tags=random.choice(error_messages))

    return render(request, 'boh/user/change_password.html', {
        'password_form': password_form,
        'active_top': 'user',
        'active_side': 'change_password'
    })


# Organization


@login_required
@require_http_methods(['GET'])
def organization_overview(request, organization_id):
    organization = get_object_or_404(Organization, pk=organization_id)

    applications = organization.application_set.all()

    return render(request, 'boh/organization/overview.html', {
        'organization': organization,
        'applications': applications,
        'active_top': 'applications',
        'active_tab': 'overview'
    })


@login_required
@require_http_methods(['GET'])
def organization_people(request, organization_id):
    organization = get_object_or_404(Organization, pk=organization_id)

    return render(request, 'boh/organization/people.html', {
        'organization': organization,
        'active_top': 'applications',
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
        messages.success(request, 'You successfully update this organization\'s general information.', extra_tags=random.choice(success_messages))

    return render(request, 'boh/organization/settings/general.html', {
        'organization': organization,
        'form': form,
        'active_top': 'applications',
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
        messages.success(request, 'You successfully deleted the "' + organization.name + '" organization.', extra_tags=random.choice(success_messages))
        return redirect('boh:dashboard.personal')

    return render(request, 'boh/organization/settings/danger.html', {
        'organization': organization,
        'active_top': 'applications',
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
        messages.success(request, 'You successfully created this organization.', extra_tags=random.choice(success_messages))
        return redirect('boh:organization.overview', organization.id)

    return render(request, 'boh/organization/add.html', {
        'form': form,
        'active_top': 'applications'
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

    return render(request, 'boh/application/list.html', {
        'applications': applications,
        'tags': tags,
        'queries': queries,
        'active_filter_tag': int(tag_id),
        'active_top': 'applications'
    })


@login_required
@require_http_methods(['GET'])
def application_overview(request, application_id):
    application = get_object_or_404(Application, pk=application_id)

    return render(request, 'boh/application/overview.html', {
        'application': application,
        'active_top': 'applications',
        'active_tab': 'overview'
    })


@login_required
@require_http_methods(['GET'])
def application_engagements(request, application_id):
    application = get_object_or_404(Application, pk=application_id)

    pending_engagements = application.engagement_set.filter(status=Engagement.PENDING_STATUS)
    open_engagements = application.engagement_set.filter(status=Engagement.OPEN_STATUS)
    closed_engagements = application.engagement_set.filter(status=Engagement.CLOSED_STATUS)

    return render(request, 'boh/application/engagements.html', {
        'application': application,
        'pending_engagements': pending_engagements,
        'open_engagements': open_engagements,
        'closed_engagements': closed_engagements,
        'active_top': 'applications',
        'active_tab': 'engagements'
    })


@login_required
@require_http_methods(['GET'])
def application_environments(request, application_id):
    application = get_object_or_404(Application, pk=application_id)

    return render(request, 'boh/application/environments.html', {
        'application': application,
        'active_top': 'applications',
        'active_tab': 'environments'
    })


@login_required
@require_http_methods(['GET'])
def application_people(request, application_id):
    application = get_object_or_404(Application, pk=application_id)

    return render(request, 'boh/application/people.html', {
        'application': application,
        'active_top': 'applications',
        'active_tab': 'people'
    })


@login_required
@require_http_methods(['GET', 'POST'])
def application_add(request):
    form = ApplicationAddForm(request.POST or None)

    if form.is_valid():
        application = form.save()
        messages.success(request, 'You successfully created this application.', extra_tags=random.choice(success_messages))
        return redirect('boh:application.overview', application_id=application.id)

    return render(request, 'boh/application/add.html', {
        'form': form,
        'active_top': 'applications'
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
                messages.success(request, 'You successfully updated this application\'s general information.', extra_tags=random.choice(success_messages))
        elif 'submit-organization' in request.POST:
            organization_form = ApplicationSettingsOrganizationForm(request.POST, instance=application)
            if organization_form.is_valid():
                organization_form.save()
                messages.success(request, 'You successfully updated this application\'s organization.', extra_tags=random.choice(success_messages))

    return render(request, 'boh/application/settings/general.html', {
        'application': application,
        'general_form': general_form,
        'organization_form': organization_form,
        'active_top': 'applications',
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
            messages.success(request, 'You successfully updated this application\'s metadata.', extra_tags=random.choice(success_messages))
    elif 'submit-tags' in request.POST:
        tags_form = ApplicationSettingsTagsForm(request.POST, instance=application)
        if tags_form.is_valid():
            tags_form.save()
            messages.success(request, 'You successfully updated this application\'s tags.', extra_tags=random.choice(success_messages))

    return render(request, 'boh/application/settings/metadata.html', {
        'application': application,
        'metadata_form': metadata_form,
        'tags_form': tags_form,
        'active_top': 'applications',
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
            messages.success(request, 'You successfully updated this application\'s data elements.', extra_tags=random.choice(success_messages))
        return redirect('boh:application.settings.data-elements', application.id)

    return render(request, 'boh/application/settings/data_elements.html', {
        'application': application,
        'data_elements_form': data_elements_form,
        'dcl_override_form': dcl_override_form,
        'dcl': application.data_classification_level,
        'dsv': application.data_sensitivity_value,
        'active_top': 'applications',
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
        messages.success(request, 'This application\'s data classification override has been updated.', extra_tags=random.choice(success_messages))

    return redirect('boh:application.settings.data-elements', application.id)


@login_required
@require_http_methods(['GET', 'POST'])
def application_settings_services(request, application_id):
    application = get_object_or_404(Application, pk=application_id)

    threadfix_form = ApplicationSettingsThreadFixForm(instance=application)

    if 'submit-threadfix' in request.POST:
        threadfix_form = ApplicationSettingsThreadFixForm(request.POST, instance=application)
        if threadfix_form.is_valid():
            threadfix_form.save()
            messages.success(request, 'You successfully updated this application\'s ThreadFix information.', extra_tags=random.choice(success_messages))

    return render(request, 'boh/application/settings/services.html', {
        'application': application,
        'threadfix_form': threadfix_form,
        'active_top': 'applications',
        'active_tab': 'settings',
        'active_side': 'services'
    })


@login_required
@require_http_methods(['GET', 'POST'])
def application_settings_danger(request, application_id):
    application = get_object_or_404(Application, pk=application_id)

    form = ApplicationDeleteForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        application.delete()
        messages.success(request, 'You successfully deleted the "' + application.name + '" application.', extra_tags=random.choice(success_messages))
        return redirect('boh:application.list')

    return render(request, 'boh/application/settings/danger.html', {
        'application': application,
        'active_top': 'applications',
        'active_tab': 'settings',
        'active_side': 'danger'
    })


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
        messages.success(request, 'You successfully created this environment.', extra_tags=random.choice(success_messages))
        return redirect('boh:application.environments', application_id=application.id)

    return render(request, 'boh/environment/add.html', {
        'application': application,
        'form': form,
        'active_top': 'applications',
        'active_tab': 'environments'
    })


@login_required
@require_http_methods(['GET', 'POST'])
def environment_edit_general(request, environment_id):
    environment = get_object_or_404(Environment, pk=environment_id)

    form = EnvironmentEditForm(request.POST or None, instance=environment)

    if form.is_valid():
        environment = form.save()
        messages.success(request, 'You successfully updated this environment.', extra_tags=random.choice(success_messages))
        return redirect('boh:environment.edit.general', environment_id=environment.id)

    return render(request, 'boh/environment/edit/general.html', {
        'application': environment.application,
        'environment': environment,
        'form': form,
        'active_top': 'applications',
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
        messages.success(request, 'You successfully updated these locations.', extra_tags=random.choice(success_messages))
        return redirect('boh:environment.edit.locations', environment_id=environment.id)

    return render(request, 'boh/environment/edit/locations.html', {
        'application': environment.application,
        'environment': environment,
        'formset': formset,
        'active_top': 'applications',
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
        messages.success(request, 'You successfully updated these credentials.', extra_tags=random.choice(success_messages))
        return redirect('boh:environment.edit.credentials', environment_id=environment.id)

    return render(request, 'boh/environment/edit/credentials.html', {
        'application': environment.application,
        'environment': environment,
        'formset': formset,
        'active_top': 'applications',
        'active_tab': 'environments',
        'active_side': 'credentials'
    })


@login_required
@require_http_methods(['GET', 'POST'])
def environment_edit_danger(request, environment_id):
    environment = get_object_or_404(Environment, pk=environment_id)

    form = EnvironmentDeleteForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        environment.delete()
        messages.success(request, 'You successfully deleted the "' + environment.get_environment_type_display() + '" environment.', extra_tags=random.choice(success_messages))
        return redirect('boh:application.environments', environment.application.id)

    return render(request, 'boh/environment/edit/danger.html', {
        'application': environment.application,
        'environment': environment,
        'active_top': 'applications',
        'active_tab': 'environments',
        'active_side': 'danger'
    })


# Engagement


@login_required
@require_http_methods(['GET'])
def engagement_detail(request, engagement_id):
    engagement = get_object_or_404(Engagement, pk=engagement_id)

    pending_activities = engagement.activity_set.filter(status=Activity.PENDING_STATUS)
    open_activities = engagement.activity_set.filter(status=Activity.OPEN_STATUS)
    closed_activities = engagement.activity_set.filter(status=Activity.CLOSED_STATUS)

    status_form = EngagementStatusForm(instance=engagement)

    comment_form = EngagementCommentAddForm()

    return render(request, 'boh/engagement/detail.html', {
        'application': engagement.application,
        'engagement': engagement,
        'pending_activities': pending_activities,
        'open_activities': open_activities,
        'closed_activities': closed_activities,
        'status_form': status_form,
        'form': comment_form,
        'active_top': 'applications',
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
        messages.success(request, 'You successfully created this engagement.', extra_tags=random.choice(success_messages))
        return redirect('boh:engagement.detail', engagement_id=engagement.id)
    else:
        return render(request, 'boh/engagement/add.html', {
            'application': application,
            'form': form,
            'active_top': 'applications',
            'active_tab': 'engagements'
        })


@login_required
@require_http_methods(['GET', 'POST'])
def engagement_edit(request, engagement_id):
    engagement = get_object_or_404(Engagement, pk=engagement_id)

    form = EngagementEditForm(request.POST or None, instance=engagement)

    if request.method == 'POST' and form.is_valid():
        engagement = form.save()
        messages.success(request, 'You successfully updated this engagement.', extra_tags=random.choice(success_messages))
        return redirect('boh:engagement.detail', engagement_id=engagement.id)

    return render(request, 'boh/engagement/edit.html', {
        'application': engagement.application,
        'engagement': engagement,
        'form': form,
        'active_top': 'applications',
        'active_tab': 'engagements'
    })


@login_required
@require_http_methods(['POST'])
def engagement_status(request, engagement_id):
    engagement = get_object_or_404(Engagement, pk=engagement_id)

    status_form = EngagementStatusForm(request.POST, instance=engagement)

    if status_form.is_valid():
        engagement = status_form.save()
        messages.success(request, 'You successfully updated this engagement\'s status to ' + engagement.get_status_display().lower() + '.', extra_tags=random.choice(success_messages))

    return redirect('boh:engagement.detail', engagement_id=engagement.id)


@login_required
@require_http_methods(['POST'])
def engagement_delete(request, engagement_id):
    engagement = get_object_or_404(Engagement, pk=engagement_id)

    form = EngagementDeleteForm(request.POST or None)

    if form.is_valid():
        engagement.delete()
        messages.success(request, 'You successfully deleted the engagement.', extra_tags='Boom!')
        return redirect('boh:application.overview', engagement.application.id)
    else:
        return redirect('boh:engagement.detail', engagement.id)


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
        messages.success(request, 'You successfully added a comment to this engagement.', extra_tags=random.choice(success_messages))

    return redirect('boh:engagement.detail', engagement_id=engagement.id)


# Activity


@login_required
@require_http_methods(['GET'])
def activity_detail(request, activity_id):
    activity = get_object_or_404(Activity, pk=activity_id)

    status_form = ActivityStatusForm(instance=activity)
    comment_form = ActivityCommentAddForm()

    return render(request, 'boh/activity/detail.html', {
        'application': activity.engagement.application,
        'activity': activity,
        'status_form': status_form,
        'form': comment_form,
        'active_top': 'applications',
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
        messages.success(request, 'You successfully added this activity.', extra_tags=random.choice(success_messages))
        return redirect('boh:activity.detail', activity_id=activity.id)
    else:
        return render(request, 'boh/activity/add.html', {
            'application': engagement.application,
            'engagement': engagement,
            'form': form,
            'active_top': 'applications',
            'active_tab': 'engagements'
        })


@login_required
@require_http_methods(['GET', 'POST'])
def activity_edit(request, activity_id):
    activity = get_object_or_404(Activity, pk=activity_id)

    form = ActivityEditForm(request.POST or None, instance=activity)

    if request.method == 'POST' and form.is_valid():
        activity = form.save()
        messages.success(request, 'You successfully updated this activity.', extra_tags=random.choice(success_messages))
        return redirect('boh:activity.detail', activity_id=activity.id)

    return render(request, 'boh/activity/edit.html', {
        'application': activity.engagement.application,
        'activity': activity,
        'form': form,
        'active_top': 'applications',
        'active_tab': 'engagements'
    })


@login_required
@require_http_methods(['POST'])
def activity_status(request, activity_id):
    activity = get_object_or_404(Activity, pk=activity_id)

    status_form = ActivityStatusForm(request.POST, instance=activity)

    if status_form.is_valid():
        activity = status_form.save()
        messages.success(request, 'You successfully updated this activity\'s status to ' + activity.get_status_display().lower() + '.', extra_tags=random.choice(success_messages))

    return redirect('boh:activity.detail', activity_id=activity.id)


@login_required
@require_http_methods(['POST'])
def activity_delete(request, activity_id):
    activity = get_object_or_404(Activity, pk=activity_id)

    form = ActivityDeleteForm(request.POST or None)

    if form.is_valid():
        activity.delete()
        messages.success(request, 'You successfully deleted the activity.', extra_tags=random.choice(success_messages))
        return redirect('boh:engagement.detail', activity.engagement.id)
    else:
        return redirect('boh:activity.detail', activity.id)


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
        messages.success(request, 'You successfully added a comment to this activity.', extra_tags=random.choice(success_messages))

    return redirect('boh:activity.detail', activity_id=activity.id)


# People


@login_required
@require_http_methods(['GET'])
def person_list(request):
    person_list = Person.objects.all()

    paginator = Paginator(person_list, 5)

    page = request.GET.get('page')
    try:
        people = paginator.page(page)
    except PageNotAnInteger:
        people = paginator.page(1)
    except EmptyPage:
        people = paginator.page(paginator.num_pages)

    return render(request, 'boh/person/list.html', {
        'people': people,
        'active_top': 'people'
    })


@login_required
@require_http_methods(['GET', 'POST'])
def person_add(request):
    form = PersonForm(request.POST or None)

    if form.is_valid():
        person = form.save()
        messages.success(request, 'You successfully created this person.', extra_tags=random.choice(success_messages))
        return redirect('boh:person.list')

    return render(request, 'boh/person/add.html', {
        'form': form,
        'active_top': 'people'
    })


@login_required
@require_http_methods(['GET'])
def person_detail(request, person_id):
    person = get_object_or_404(Person, pk=person_id)

    return render(request, 'boh/person/detail.html', {
        'person': person,
        'active_top': 'people'
    })


@login_required
@require_http_methods(['GET', 'POST'])
def person_edit(request, person_id):
    person = get_object_or_404(Person, pk=person_id)

    form = PersonForm(request.POST or None, instance=person)

    if request.method == 'POST':
        if form.is_valid():
            person = form.save()
            messages.success(request, 'You successfully updated ' + person.first_name + ' ' + person.last_name + '.', extra_tags=random.choice(success_messages))
            return redirect('boh:person.detail', person.id)
        else:
            messages.error(request, 'There was a problem updating' + person.first_name + ' ' + person.last_name + '.', extra_tags=random.choice(error_messages))

    return render(request, 'boh/person/edit.html', {
        'person': person,
        'form': form,
        'active_top': 'people'
    })


@login_required
@require_http_methods(['POST'])
def person_delete(request, person_id):
    person = get_object_or_404(Person, pk=person_id)

    form = PersonDeleteForm(request.POST or None)

    if form.is_valid():
        person.delete()
        messages.success(request, 'You successfully deleted ' + person.first_name + ' ' + person.last_name + '.', extra_tags=random.choice(success_messages))
        return redirect('boh:person.list')
    else:
        return redirect('boh:person.detail', person.id)
