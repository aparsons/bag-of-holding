import random

from django import forms as django_forms
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.admin.views.decorators import staff_member_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.urlresolvers import reverse
from django.db import IntegrityError
from django.db.models import Avg, Count, Prefetch, Q
from django.forms.formsets import formset_factory
from django.forms.models import inlineformset_factory
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from django.shortcuts import get_object_or_404, render, redirect
from django.views.decorators.http import require_http_methods

from . import filters, forms, models, reports

from threadfix_api import threadfix as tf_api


# Messages shown on successful actions
success_messages = [
    ':D',
    'Alrighty Then!',
    'Awesome!',
    'Bam!',
    'Behold!',
    'Bingo!',
    'Boom Chuck!',
    'Cheers!',
    'Choo Choo!',
    'Excellent!',
    'Good Show!',
    'Great!',
    'Hey!',
    'Huzzah!',
    'Kudos!',
    'Nice!',
    'Presto!',
    'Shazzam!',
    'Success!',
    'Well Done!',
    'Whack!',
    'Whoa!',
    'Yay!',
    'Zowie!',
]

error_messages = [
    'Crud!',
    'Darn!',
    'Oopsey!',
    'Pshaw!',
    'Rats!',
    'Uh-oh!',
    'Whoops!',
    'Yikes!'
]


# Dashboard

@login_required
@require_http_methods(['GET'])
def dashboard_personal(request):
    """The personal dashboard with information relevant to the current user."""

    activities = models.Activity.objects.filter(users__id=request.user.id) \
        .select_related('activity_type__name') \
        .select_related('engagement') \
        .select_related('engagement__application__name') \
        .annotate(comment_count=Count('activitycomment'))

    pending_activities = activities.filter(status=models.Engagement.PENDING_STATUS)
    open_activities = activities.filter(status=models.Engagement.OPEN_STATUS)

    return render(request, 'boh/dashboard/my_dashboard.html', {
        'pending_activities': pending_activities,
        'open_activities': open_activities,
        'active_top': 'dashboard',
        'active_tab': 'personal'
    })


@login_required
@require_http_methods(['GET'])
def dashboard_team(request):
    # Find open and pending activities by user
    activities_by_user = User.objects.all().prefetch_related(
        Prefetch('activity_set', queryset=models.Activity.objects
            .filter(~Q(status=models.Activity.CLOSED_STATUS))
            .select_related('activity_type__name')
            .select_related('engagement')
            .annotate(comment_count=Count('activitycomment'))
            .select_related('engagement__application__name')
        )
    )

    # Find open and pending engagements
    engagements = models.Engagement.objects.all().prefetch_related(
        Prefetch('activity_set', queryset=models.Activity.objects.all()
            .select_related('activity_type__name')
            .annotate(user_count=Count('users'))
        )
    ).select_related('application__name').annotate(comment_count=Count('engagementcomment'))

    open_engagements = engagements.filter(status=models.Engagement.OPEN_STATUS)
    pending_engagements = engagements.filter(status=models.Engagement.PENDING_STATUS)

    # Find activities where no user is assigned
    unassigned_activities = models.Activity.objects.filter(users=None) \
        .select_related('activity_type__name') \
        .select_related('engagement') \
        .select_related('engagement__application__name') \
        .annotate(comment_count=Count('activitycomment'))

    # Find engagements where no activities have been created
    empty_engagements = models.Engagement.objects.filter(activity__isnull=True) \
        .select_related('application__name') \
        .prefetch_related('activity_set') \
        .annotate(comment_count=Count('engagementcomment'))

    return render(request, 'boh/dashboard/team_dashboard.html', {
        'activities_by_user': activities_by_user,
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
    year = None

    year_form = forms.MetricsYearForm(request.GET)
    if year_form.is_valid():
        year = year_form.cleaned_data['year']

    engagement_stats = models.Engagement.metrics.stats(year)
    activity_stats = models.ActivityType.metrics.stats(year)

    return render(request, 'boh/dashboard/metrics.html', {
        'year_form': year_form,
        'engagement_stats': engagement_stats,
        'activity_stats': activity_stats,
        'active_top': 'dashboard',
        'active_tab': 'metrics'
    })


@login_required
@require_http_methods(['GET'])
def dashboard_reports(request):

    # BISO Reports
    # Top 10 Reports
    ec_report_form = forms.EngagementCoverageReportForm()
    tf_report_form = forms.ThreadFixSummaryReportForm()
    as_report_form = forms.AppSummaryReportForm()

    return render(request, 'boh/dashboard/reports.html', {
        'ec_report_form': ec_report_form,
        'tf_report_form': tf_report_form,
        'as_report_form': as_report_form,
        'active_top': 'dashboard',
        'active_tab': 'reports'
    })

@login_required
@require_http_methods(['POST'])
def dashboard_reports_download(request):
    timestamp = timezone.now().strftime('%y%m%d%H%M%S')

    report_type = request.GET.get('report_type')
    if report_type == 'engagement_coverage':
        form = forms.EngagementCoverageReportForm(request.POST)
        if form.is_valid():
            file_name = 'engagement-coverage_' + timestamp
            return reports.EngagementCoverageReport(file_name, form.cleaned_data['format'], form.cleaned_data['organizations'], request.user).response()
    elif report_type == 'threadfix_summary':
        form = forms.ThreadFixSummaryReportForm(request.POST)
        if form.is_valid():
            file_name = 'threadfix-summary_' + timestamp
            return reports.ThreadFixSummaryReport(file_name, form.cleaned_data['format'], form.cleaned_data['organizations'], request.user).response()
    elif report_type == 'app_summary':
        form = forms.AppSummaryReportForm(request.POST)
        if form.is_valid():
            file_name = 'app-summary_' + timestamp
            return reports.AppSummaryReport(file_name, form.cleaned_data['format'], form.cleaned_data['applications'], request.user).response()

    messages.error(request, _('There was a problem downloading the report.'), extra_tags=random.choice(error_messages))
    return redirect('boh:dashboard.reports')

# Management

@login_required
@staff_member_required
@require_http_methods(['GET'])
def management_overview(request):
    threadfix_services = models.ThreadFix.objects.all()

    return render(request, 'boh/management/overview.html', {
        'threadfix_services': threadfix_services,
        'active_top': 'management',
        'active_side': 'overview'
    })


@login_required
@staff_member_required
@require_http_methods(['GET'])
def management_application_tags(request):
    tags = models.Tag.objects.all()

    return render(request, 'boh/management/application_tags/application_tags.html', {
        'tags': tags,
        'active_top': 'management',
        'active_side': 'tags'
    })


@login_required
@staff_member_required
@require_http_methods(['GET', 'POST'])
def management_application_tags_add(request):
    add_form = forms.ApplicationTagForm(request.POST or None)

    if request.method == 'POST':
        if add_form.is_valid():
            tag = add_form.save()
            messages.success(request, _('You successfully added the "%(tag_name)s" application tag.') % {'tag_name': tag.name}, extra_tags=random.choice(success_messages))
            return redirect('boh:management.tags')
        else:
            messages.error(request, _('There was a problem creating this application tag.'), extra_tags=random.choice(error_messages))

    return render(request, 'boh/management/application_tags/add.html', {
        'add_form': add_form,
        'active_top': 'management',
        'active_side': 'tags'
    })


@login_required
@staff_member_required
@require_http_methods(['GET', 'POST'])
def management_application_tags_edit(request, tag_id):
    tag = get_object_or_404(models.Tag, pk=tag_id)

    edit_form = forms.ApplicationTagForm(request.POST or None, instance=tag)

    if request.method == 'POST':
        if edit_form.is_valid():
            tag = edit_form.save()
            messages.success(request, _('You successfully updated the "%(tag_name)s" application tag.') % {'tag_name': tag.name}, extra_tags=random.choice(success_messages))
            return redirect('boh:management.tags')
        else:
            messages.error(request, _('There was a problem updating this application tag.'), extra_tags=random.choice(error_messages))

    return render(request, 'boh/management/application_tags/edit.html', {
        'tag': tag,
        'edit_form': edit_form,
        'active_top': 'management',
        'active_side': 'tags'
    })


@login_required
@staff_member_required
@require_http_methods(['POST'])
def management_application_tags_delete(request, tag_id):
    tag = get_object_or_404(models.Tag, pk=tag_id)

    form = forms.ApplicationTagDeleteForm(request.POST, instance=tag)

    if form.is_valid():
        tag.delete()
        messages.success(request, _('You successfully deleted the "%(tag_name)s" application tag.') % {'tag_name': tag.name}, extra_tags=random.choice(success_messages))
        return redirect('boh:management.tags')
    else:
        messages.error(request, _('There was a problem deleting this application tag.'), extra_tags=random.choice(error_messages))
        return redirect('boh:management.tags.edit', tag.id)


@login_required
@staff_member_required
@require_http_methods(['GET'])
def management_activity_types(request):
    activity_types = models.ActivityType.objects.all()

    return render(request, 'boh/management/activity_types/activity_types.html', {
        'activity_types': activity_types,
        'active_top': 'management',
        'active_side': 'activity_types'
    })


@login_required
@staff_member_required
@require_http_methods(['GET', 'POST'])
def management_activity_types_add(request):
    activity_type_form = forms.ActivityTypeForm(request.POST or None)

    if request.method == 'POST':
        if activity_type_form.is_valid():
            activity_type = activity_type_form.save()
            messages.success(request, _('You successfully created the "%(activity_type_name)s" activity type.') % {'activity_type_name': activity_type.name}, extra_tags=random.choice(success_messages))
            return redirect('boh:management.activity_types')
        else:
            messages.error(request, _('There was a problem creating this activity type.'), extra_tags=random.choice(error_messages))

    return render(request, 'boh/management/activity_types/add.html', {
        'activity_type_form': activity_type_form,
        'active_top': 'management',
        'active_side': 'activity_types'
    })


@login_required
@staff_member_required
@require_http_methods(['GET'])
def management_activity_types_documentation(request, activity_type_id):
    activity_type = get_object_or_404(models.ActivityType, pk=activity_type_id)

    return render(request, 'boh/management/activity_types/documentation.html', {
        'activity_type': activity_type,
        'active_top': 'management',
        'active_side': 'activity_types'
    })


@login_required
@staff_member_required
@require_http_methods(['GET', 'POST'])
def management_activity_types_edit(request, activity_type_id):
    activity_type = get_object_or_404(models.ActivityType, pk=activity_type_id)

    activity_type_form = forms.ActivityTypeForm(request.POST or None, instance=activity_type)

    if request.method == 'POST':
        if activity_type_form.is_valid():
            activity_type = activity_type_form.save()
            messages.success(request, _('You successfully updated the "%(activity_type_name)s" activity type.') % {'activity_type_name': activity_type.name}, extra_tags=random.choice(success_messages))
            return redirect('boh:management.activity_types')
        else:
            messages.error(request, _('There was a problem updating this activity type.'), extra_tags=random.choice(error_messages))

    return render(request, 'boh/management/activity_types/edit.html', {
        'activity_type': activity_type,
        'activity_type_form': activity_type_form,
        'active_top': 'management',
        'active_side': 'activity_types'
    })


@login_required
@staff_member_required
@require_http_methods(['POST'])
def management_activity_types_delete(request, activity_type_id):
    activity_type = get_object_or_404(models.ActivityType, pk=activity_type_id)

    form = forms.ActivityTypeDeleteForm(request.POST, instance=activity_type)

    if form.is_valid():
        activity_type.delete()
        messages.success(request, _('You successfully deleted the "%(activity_type_name)s" activity type.') % {'activity_type_name': activity_type.name}, extra_tags=random.choice(success_messages))
        return redirect('boh:management.activity_types')
    else:
        messages.error(request, _('There was a problem deleting this activity type.'), extra_tags=random.choice(error_messages))
        return redirect('boh:management.activity_types.edit', activity_type.id)


@login_required
@staff_member_required
@require_http_methods(['GET'])
def management_services(request):
    threadfix_services = models.ThreadFix.objects.all()

    return render(request, 'boh/management/services.html', {
        'threadfix_services': threadfix_services,
        'active_top': 'management',
        'active_side': 'services'
    })


@login_required
@staff_member_required
@require_http_methods(['GET', 'POST'])
def management_services_threadfix_add(request):
    threadfix_form = forms.ThreadFixForm(request.POST or None)

    if request.method == 'POST':
        if threadfix_form.is_valid():
            threadfix = threadfix_form.save()
            messages.success(request, _('You successfully created the "%(threadfix_name)s" ThreadFix service.') % {'threadfix_name': threadfix.name}, extra_tags=random.choice(success_messages))
            return redirect('boh:management.services')
        else:
            messages.error(request, _('There was a problem creating this ThreadFix service.'), extra_tags=random.choice(error_messages))

    return render(request, 'boh/management/threadfix/add.html', {
        'threadfix_form': threadfix_form,
        'active_top': 'management',
        'active_side': 'services'
    })


@login_required
@staff_member_required
@require_http_methods(['GET', 'POST'])
def management_services_threadfix_edit(request, threadfix_id):
    threadfix = get_object_or_404(models.ThreadFix, pk=threadfix_id)

    threadfix_form = forms.ThreadFixForm(request.POST or None, instance=threadfix)

    if request.method == 'POST':
        if threadfix_form.is_valid():
            threadfix = threadfix_form.save()
            messages.success(request, _('You successfully updated the "%(threadfix_name)s" ThreadFix service.') % {'threadfix_name': threadfix.name}, extra_tags=random.choice(success_messages))
            return redirect('boh:management.services')
        else:
            messages.error(request, _('There was a problem updating this ThreadFix service.'), extra_tags=random.choice(error_messages))

    return render(request, 'boh/management/threadfix/edit.html', {
        'threadfix': threadfix,
        'threadfix_form': threadfix_form,
        'active_top': 'management',
        'active_side': 'services'
    })


@login_required
@staff_member_required
@require_http_methods(['GET'])
def management_services_threadfix_test(request, threadfix_id):
    threadfix = get_object_or_404(models.ThreadFix, pk=threadfix_id)

    api = tf_api.ThreadFixAPI(host=threadfix.host, api_key=threadfix.api_key, verify_ssl=threadfix.verify_ssl)
    response = api.list_teams()

    if response.success:
        messages.success(request, _('Everything appears to be working correctly for the "%(threadfix_name)s" ThreadFix service.') % {'threadfix_name': threadfix.name}, extra_tags=random.choice(success_messages))
    else:
        messages.error(request, _('An error occurred when testing "%(threadfix_name)s". Error message: %(error)s') % {'threadfix_name': threadfix.name, 'error': response.message}, extra_tags=random.choice(error_messages))

    return redirect('boh:management.services')


@login_required
@staff_member_required
@require_http_methods(['GET', 'POST'])
def management_services_threadfix_import(request, threadfix_id):
    threadfix = get_object_or_404(models.ThreadFix, pk=threadfix_id)

    ImportFormSet = formset_factory(forms.ThreadFixApplicationImportForm, extra=0)

    if request.method == 'GET':
        api = tf_api.ThreadFixAPI(host=threadfix.host, api_key=threadfix.api_key, verify_ssl=threadfix.verify_ssl)
        teams_response = api.list_teams()

        if teams_response.success:
            import_applications = []
            application_count = 0

            for json_team in teams_response.data:
                for json_application in json_team['applications']:
                    application = {'team_id': json_team['id'], 'team_name': json_team['name'][:128], 'application_name': json_application['name'][:128], 'application_id': json_application['id']}
                    import_applications.append(application)
                    application_count += 1

            import_formset = ImportFormSet(initial=import_applications)

            return render(request, 'boh/management/threadfix/import.html', {
                'threadfix': threadfix,
                'import_formset': import_formset,
                'active_top': 'management',
                'active_side': 'services'
            })
        else:
            messages.error(request, _('An error occurred when importing from "%(threadfix_name)s". Error message: %(error)s') % {'threadfix_name': threadfix.name, 'error': teams_response.message}, extra_tags=random.choice(error_messages))
            return redirect('boh:management.services')
    elif request.method == 'POST':
        import_formset = ImportFormSet(request.POST)

        imported_applications = []
        failed_applications = []
        if import_formset.is_valid():
            for form in import_formset.cleaned_data:
                if form['organization']:
                    application = models.Application(name=form['application_name'], organization=form['organization'], threadfix=threadfix, threadfix_team_id=form['team_id'], threadfix_application_id=form['application_id'])
                    try:
                        application.save()
                        imported_applications.append(application)
                    except IntegrityError:
                        failed_applications.append(application)

            if len(imported_applications) > 0 or len(failed_applications) > 0:
                return render(request, 'boh/management/threadfix/import_done.html', {
                    'threadfix': threadfix,
                    'imported_applications': imported_applications,
                    'failed_applications': failed_applications,
                    'active_top': 'management',
                    'active': 'services'
                })
            else:
                messages.warning(request, _('No applications were imported from "%(threadfix_name)s".') % {'threadfix_name': threadfix.name}, extra_tags=random.choice(error_messages))
        else:
            messages.error(request, _('An error occurred when saving the import from "%(threadfix_name)s".') % {'threadfix_name': threadfix.name}, extra_tags=random.choice(error_messages))

        return redirect('boh:management.services')


@login_required
@staff_member_required
@require_http_methods(['POST'])
def management_services_threadfix_delete(request, threadfix_id):
    threadfix = get_object_or_404(models.ThreadFix, pk=threadfix_id)

    form = forms.ThreadFixDeleteForm(request.POST, instance=threadfix)

    if form.is_valid():
        threadfix.delete()
        messages.success(request, _('You successfully deleted the "%(threadfix_name)s" ThreadFix service.') % {'threadfix_name': threadfix.name}, extra_tags=random.choice(success_messages))
        return redirect('boh:management.services')
    else:
        messages.error(request, _('There was a problem deleting this ThreadFix service.'), extra_tags=random.choice(error_messages))
        return redirect('boh:management.services.threadfix.edit', threadfix.id)


@login_required
@staff_member_required
@require_http_methods(['GET'])
def management_users(request):

    return render(request, 'boh/management/users.html', {
        'active_top': 'management',
        'active_side': 'users'
    })


# User


@login_required
@require_http_methods(['GET', 'POST'])
def user_profile(request):
    profile_form = forms.UserProfileForm(request.POST or None, instance=request.user)

    if request.method == 'POST':
        if profile_form.is_valid():
            profile_form.save()
            messages.success(request, _('You successfully updated your profile.'), extra_tags=random.choice(success_messages))
        else:
            messages.error(request, _('There was a problem updating your profile.'), extra_tags=random.choice(error_messages))

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
            messages.success(request, _('You successfully changed your password.'), extra_tags=random.choice(success_messages))
        else:
            messages.error(request, _('There was a problem changing your password.'), extra_tags=random.choice(error_messages))

    return render(request, 'boh/user/change_password.html', {
        'password_form': password_form,
        'active_top': 'user',
        'active_side': 'change_password'
    })


# Organization


@login_required
@require_http_methods(['GET'])
def organization_overview(request, organization_id):
    organization = get_object_or_404(models.Organization, pk=organization_id)

    return render(request, 'boh/organization/overview.html', {
        'organization': organization,
        'active_top': 'applications',
        'active_tab': 'overview'
    })


@login_required
@require_http_methods(['GET'])
def organization_applications(request, organization_id):
    organization = get_object_or_404(models.Organization, pk=organization_id)

    return render(request, 'boh/organization/applications.html', {
        'organization': organization,
        'active_top': 'applications',
        'active_tab': 'applications'
    })


@login_required
@require_http_methods(['GET'])
def organization_people(request, organization_id):
    organization = get_object_or_404(models.Organization, pk=organization_id)

    return render(request, 'boh/organization/people.html', {
        'organization': organization,
        'active_top': 'applications',
        'active_tab': 'people'
    })


@login_required
@require_http_methods(['GET', 'POST'])
def organization_settings_general(request, organization_id):
    organization = get_object_or_404(models.Organization, pk=organization_id)

    form = forms.OrganizationSettingsGeneralForm(request.POST or None, instance=organization)

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, _('You successfully updated this organization\'s general information.'), extra_tags=random.choice(success_messages))
        else:
            messages.error(request, _('There was a problem updating this organization\'s general information.'), extra_tags=random.choice(error_messages))

    return render(request, 'boh/organization/settings/general.html', {
        'organization': organization,
        'form': form,
        'active_top': 'applications',
        'active_tab': 'settings',
        'active_side': 'general'
    })


@login_required
@require_http_methods(['GET', 'POST'])
def organization_settings_people(request, organization_id):
    organization = get_object_or_404(models.Organization, pk=organization_id)

    people_form = forms.OrganizationSettingsPeopleForm(request.POST or None, instance=organization)

    if request.method == 'POST':
        if people_form.is_valid():
            people_form.save()
            messages.success(request, _('You successfully updated this organization\'s associated people.'), extra_tags=random.choice(success_messages))
        else:
            messages.error(request, _('There was a problem updating this organization\'s associated people.'), extra_tags=random.choice(error_messages))

    return render(request, 'boh/organization/settings/people.html', {
        'organization': organization,
        'people_form': people_form,
        'active_top': 'applications',
        'active_tab': 'settings',
        'active_side': 'people'
    })


@login_required
@require_http_methods(['GET', 'POST'])
def organization_settings_danger(request, organization_id):
    organization = get_object_or_404(models.Organization, pk=organization_id)

    form = forms.OrganizationDeleteForm(request.POST or None, instance=organization)

    if request.method == 'POST' and form.is_valid():
        organization.delete()
        messages.success(request, _('You successfully deleted the "%(organization_name)s" organization.') % {'organization_name': organization.name}, extra_tags=random.choice(success_messages))
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
    form = forms.OrganizationAddForm(request.POST or None)

    if form.is_valid():
        organization = form.save()
        messages.success(request, _('You successfully created this organization.'), extra_tags=random.choice(success_messages))
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
    if queries.__contains__('page_size'):
        del queries['page_size']

    application_filter = filters.ApplicationFilter(request.GET, queryset=models.Application.objects.all().select_related('organization__name').prefetch_related('tags'))

    page_size = 25

    page_size_form = forms.PageSizeForm()
    if request.GET.get('page_size'):
        page_size_form = forms.PageSizeForm(request.GET)
        if page_size_form.is_valid():
            page_size = page_size_form.cleaned_data['page_size']
            if page_size == 'all':
                page_size = 10000000
            else:
                page_size = int(page_size)

    paginator = Paginator(application_filter, page_size)

    page = request.GET.get('page')

    try:
        applications = paginator.page(page)
    except PageNotAnInteger:
        applications = paginator.page(1)
    except EmptyPage:
        applications = paginator.page(paginator.num_pages)

    #
    show_advanced = False
    if request.GET.get('platform') or request.GET.get('lifecycle') or request.GET.get('origin') or request.GET.get('technologies') or request.GET.get('regulations') or request.GET.get('tags') or request.GET.get('service_level_agreements') or request.GET.get('asvs_level') or (request.GET.get('external_audience') and request.GET.get('external_audience') is not '1') or (request.GET.get('internet_accessible') and request.GET.get('internet_accessible') is not '1'):
        show_advanced = True

    return render(request, 'boh/application/list.html', {
        'form': application_filter.form,
        'applications': applications,
        'queries': queries,
        'page_size_form': page_size_form,
        'page_size': str(page_size),
        'show_advanced': show_advanced,
        'active_top': 'applications'
    })


@login_required
@require_http_methods(['GET'])
def application_overview(request, application_id):
    application = get_object_or_404(models.Application, pk=application_id)

    return render(request, 'boh/application/overview.html', {
        'application': application,
        'active_top': 'applications',
        'active_tab': 'overview'
    })


@login_required
@require_http_methods(['GET'])
def application_engagements(request, application_id):
    application = get_object_or_404(models.Application.objects.select_related('organization'), pk=application_id)

    engagements = application.engagement_set.prefetch_related(
        Prefetch('activity_set', queryset=models.Activity.objects
            .all()
            .select_related('activity_type__name')
        )
    ).annotate(comment_count=Count('engagementcomment'))

    pending_engagements = engagements.filter(status=models.Engagement.PENDING_STATUS)
    open_engagements = engagements.filter(status=models.Engagement.OPEN_STATUS)
    closed_engagements = engagements.filter(status=models.Engagement.CLOSED_STATUS).order_by('-end_date')

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
    application = get_object_or_404(models.Application, pk=application_id)

    return render(request, 'boh/application/environments.html', {
        'application': application,
        'active_top': 'applications',
        'active_tab': 'environments'
    })


@login_required
@require_http_methods(['GET'])
def application_people(request, application_id):
    application = get_object_or_404(models.Application, pk=application_id)

    return render(request, 'boh/application/people.html', {
        'application': application,
        'active_top': 'applications',
        'active_tab': 'people'
    })


@login_required
@require_http_methods(['GET', 'POST'])
def application_people_add(request, application_id):
    application = get_object_or_404(models.Application, pk=application_id)

    relation_form = forms.PersonRelationForm(request.POST or None)
    relation_form.fields['person'].queryset = models.Person.objects.exclude(application__id=application.id)

    if request.method == 'POST':
        if relation_form.is_valid():
            relation = relation_form.save(commit=False)
            relation.application = application
            name = relation.person.first_name + ' ' + relation.person.last_name
            try:
                relation.save()
            except IntegrityError:
                messages.error(request, _('"%(name)s" is already related to this application.') % {'name': name}, extra_tags=random.choice(error_messages))
            else:
                messages.success(request, _('You successfully added "%(name)s" to this application.') % {'name': name}, extra_tags=random.choice(success_messages))
            finally:
                return redirect('boh:application.people', application.id)
        else:
            messages.error(request, _('There was a problem saving the relation to this application.'), extra_tags=random.choice(error_messages))

    return render(request, 'boh/application/add_relation.html', {
        'application': application,
        'relation_form': relation_form,
        'active_top': 'applications',
        'active_tab': 'people'
    })


@login_required
@require_http_methods(['GET', 'POST'])
def application_people_edit(request, application_id, relation_id):
    application = get_object_or_404(models.Application, pk=application_id)
    relation = get_object_or_404(models.Relation, pk=relation_id)

    relation_form = forms.PersonRelationForm(request.POST or None, instance=relation)
    relation_form.fields['person'].queryset = models.Person.objects.exclude(Q(application__id=application.id) & ~Q(id=relation.person.id))
    relation_form.fields['person'].value = relation.person

    if request.method == 'POST':
        if relation_form.is_valid():
            relation = relation_form.save(commit=False)
            relation.application = application
            name = relation.person.first_name + ' ' + relation.person.last_name
            try:
                relation.save()
            except IntegrityError:
                messages.error(request, _('"%(name)s" is already related to this application.') % {'name': name}, extra_tags=random.choice(error_messages))
            else:
                messages.success(request, _('You successfully added "%(name)s" to this application.') % {'name': name}, extra_tags=random.choice(success_messages))
            finally:
                return redirect('boh:application.people', application.id)
        else:
            messages.error(request, _('There was a problem saving the relation to this application.'), extra_tags=random.choice(error_messages))

    return render(request, 'boh/application/edit_relation.html', {
        'application': application,
        'relation': relation,
        'relation_form': relation_form,
        'active_top': 'applications',
        'active_tab': 'people'
    })


@login_required
@require_http_methods(['POST'])
def application_people_delete(request, application_id, relation_id):
    application = get_object_or_404(models.Application, pk=application_id)
    relation = get_object_or_404(models.Relation, pk=relation_id)
    name = relation.person.first_name + ' ' + relation.person.last_name

    delete_form = forms.RelationDeleteForm(request.POST, instance=relation)

    if delete_form.is_valid():
        relation.delete()
        messages.success(request, _('You successfully disassociated "%(name)s" with this application.') % {'name': name}, extra_tags=random.choice(success_messages))
    else:
        messages.error(request, _('There was a problem disassociating "%(name)s" with this application.') % {'name': name}, extra_tags=random.choice(error_messages))

    return redirect('boh:application.people', application.id)


@login_required
@require_http_methods(['GET', 'POST'])
def application_add(request):
    form = forms.ApplicationAddForm(request.POST or None)

    if form.is_valid():
        application = form.save()
        messages.success(request, _('You successfully created this application.'), extra_tags=random.choice(success_messages))
        return redirect('boh:application.overview', application_id=application.id)

    return render(request, 'boh/application/add.html', {
        'form': form,
        'active_top': 'applications'
    })


@login_required
@require_http_methods(['GET', 'POST'])
def application_settings_general(request, application_id):
    application = get_object_or_404(models.Application, pk=application_id)

    general_form = forms.ApplicationSettingsGeneralForm(instance=application)
    organization_form = forms.ApplicationSettingsOrganizationForm(instance=application)

    if request.method == 'POST':
        if 'submit-general' in request.POST:
            general_form = forms.ApplicationSettingsGeneralForm(request.POST, instance=application)
            if general_form.is_valid():
                general_form.save()
                messages.success(request, _('You successfully updated this application\'s general information.'), extra_tags=random.choice(success_messages))
        elif 'submit-organization' in request.POST:
            organization_form = forms.ApplicationSettingsOrganizationForm(request.POST, instance=application)
            if organization_form.is_valid():
                organization_form.save()
                messages.success(request, _('You successfully updated this application\'s organization.'), extra_tags=random.choice(success_messages))

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
    application = get_object_or_404(models.Application, pk=application_id)

    metadata_form = forms.ApplicationSettingsMetadataForm(instance=application)
    technologies_form = forms.ApplicationSettingsTechnologiesForm(instance=application)
    regulations_form = forms.ApplicationSettingsRegulationsForm(instance=application)
    tags_form = forms.ApplicationSettingsTagsForm(instance=application)

    if 'submit-metadata' in request.POST:
        metadata_form = forms.ApplicationSettingsMetadataForm(request.POST, instance=application)
        if metadata_form.is_valid():
            metadata_form.save()
            messages.success(request, _('You successfully updated this application\'s metadata.'), extra_tags=random.choice(success_messages))
        else:
            messages.error(request, _('There was a problem updating this application\'s metadata.'), extra_tags=random.choice(error_messages))
    if 'submit-technologies' in request.POST:
        technologies_form = forms.ApplicationSettingsTechnologiesForm(request.POST, instance=application)
        if technologies_form.is_valid():
            technologies_form.save()
            messages.success(request, _('You successfully updated this application\'s technologies.'), extra_tags=random.choice(success_messages))
        else:
            messages.error(request, _('There was a problem updating this application\'s technologies.'), extra_tags=random.choice(error_messages))
    if 'submit-regulations' in request.POST:
        regulations_form = forms.ApplicationSettingsRegulationsForm(request.POST, instance=application)
        if regulations_form.is_valid():
            regulations_form.save()
            messages.success(request, _('You successfully updated this application\'s regulations.'), extra_tags=random.choice(success_messages))
        else:
            messages.error(request, _('There was a problem updating this application\'s regulations.'), extra_tags=random.choice(error_messages))
    elif 'submit-tags' in request.POST:
        tags_form = forms.ApplicationSettingsTagsForm(request.POST, instance=application)
        if tags_form.is_valid():
            tags_form.save()
            messages.success(request, _('You successfully updated this application\'s tags.'), extra_tags=random.choice(success_messages))
        else:
            messages.error(request, _('There was a problem updating this application\'s tags.'), extra_tags=random.choice(error_messages))

    return render(request, 'boh/application/settings/metadata.html', {
        'application': application,
        'metadata_form': metadata_form,
        'technologies_form': technologies_form,
        'regulations_form': regulations_form,
        'tags_form': tags_form,
        'active_top': 'applications',
        'active_tab': 'settings',
        'active_side': 'metadata'
    })


@login_required
@require_http_methods(['GET', 'POST'])
def application_settings_data_elements(request, application_id):
    application = get_object_or_404(models.Application, pk=application_id)

    data_elements_form = forms.ApplicationSettingsDataElementsForm(request.POST or None, instance=application)
    dcl_override_form = forms.ApplicationSettingsDCLOverrideForm(instance=application)

    if request.method == 'POST':
        if data_elements_form.is_valid():
            data_elements_form.save()
            messages.success(request, _('You successfully updated this application\'s data elements.'), extra_tags=random.choice(success_messages))
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
@require_http_methods(['GET', 'POST'])
def application_settings_service_level_agreements(request, application_id):
    application = get_object_or_404(models.Application, pk=application_id)

    sla_form = forms.ApplicationSettingsServiceLevelAgreementForm(request.POST or None, instance=application)

    if request.method == 'POST':
        if sla_form.is_valid():
            sla_form.save()
            messages.success(request, _('You successfully updated this application\'s service level agreements.'), extra_tags=random.choice(success_messages))
        else:
            messages.error(request, _('There was a problem updating this application\'s service level agreements.'), extra_tags=random.choice(error_messages))

    return render(request, 'boh/application/settings/service_level_agreements.html', {
        'application': application,
        'sla_form': sla_form,
        'active_top': 'applications',
        'active_tab': 'settings',
        'active_side': 'agreements'
    })


@login_required
@require_http_methods(['POST'])
def application_settings_data_elements_override(request, application_id):
    application = get_object_or_404(models.Application, pk=application_id)

    dcl_override_form = forms.ApplicationSettingsDCLOverrideForm(request.POST or None, instance=application)

    if dcl_override_form.is_valid():
        dcl_override_form.save()
        messages.success(request, _('This application\'s data classification override has been updated.'), extra_tags=random.choice(success_messages))

    return redirect('boh:application.settings.data-elements', application.id)


@login_required
@require_http_methods(['GET', 'POST'])
def application_settings_services(request, application_id):
    application = get_object_or_404(models.Application, pk=application_id)

    threadfix_form = forms.ApplicationSettingsThreadFixForm(instance=application)

    if 'submit-threadfix' in request.POST:
        threadfix_form = forms.ApplicationSettingsThreadFixForm(request.POST, instance=application)
        if threadfix_form.is_valid():
            threadfix_form.save()
            messages.success(request, _('You successfully updated this application\'s ThreadFix information.'), extra_tags=random.choice(success_messages))

    return render(request, 'boh/application/settings/services.html', {
        'application': application,
        'threadfix_form': threadfix_form,
        'active_top': 'applications',
        'active_tab': 'settings',
        'active_side': 'services'
    })

@login_required
@require_http_methods(['GET', 'POST'])
def application_settings_owasp_asvs(request, application_id):
    application = get_object_or_404(models.Application, pk=application_id)

    asvs_form = forms.ApplicationSettingsASVSForm(instance=application)

    if 'submit-asvs' in request.POST:
        asvs_form = forms.ApplicationSettingsASVSForm(request.POST, instance=application)
        if asvs_form.is_valid():
            asvs_form.save()
            messages.success(request, _('You successfully updated this application\'s ASVS information.'), extra_tags=random.choice(success_messages))

    return render(request, 'boh/application/settings/owasp_asvs.html', {
        'application': application,
        'asvs_form': asvs_form,
        'active_top': 'applications',
        'active_tab': 'settings',
        'active_side': 'owasp'
    })


@login_required
@require_http_methods(['GET', 'POST'])
def application_settings_custom_fields(request, application_id):
    application = get_object_or_404(models.Application, pk=application_id)

    ApplicationCustomFieldValueFormSet = \
        inlineformset_factory(
            models.Application,
            models.ApplicationCustomFieldValue,
            fields=('custom_field', 'value',),
            extra=1,
            widgets={}
        )

    formset = ApplicationCustomFieldValueFormSet(request.POST or None, instance=application)

    if formset.is_valid():
        formset.save()
        messages.success(request, _('You successfully updated these custom fields.'), extra_tags=random.choice(success_messages))
        return redirect('boh:application.settings.custom-fields', application_id=application.id)

    custom_fields = models.CustomField.objects.all()

    return render(request, 'boh/application/settings/custom_fields.html', {
        'application': application,
        'custom_fields': custom_fields,
        'formset': formset,
        'active_top': 'applications',
        'active_tab': 'settings',
        'active_side': 'custom_fields'
    })


@login_required
@require_http_methods(['GET', 'POST'])
def application_settings_danger(request, application_id):
    application = get_object_or_404(models.Application, pk=application_id)

    form = forms.ApplicationDeleteForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        application.delete()
        messages.success(request, _('You successfully deleted the "%(application_name)s" application.') % {'application_name': application.name}, extra_tags=random.choice(success_messages))
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
    application = get_object_or_404(models.Application, pk=application_id)

    form = forms.EnvironmentAddForm(request.POST or None)

    if form.is_valid():
        environment = form.save(commit=False)
        environment.application = application
        environment.save()
        messages.success(request, _('You successfully created this environment.'), extra_tags=random.choice(success_messages))
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
    environment = get_object_or_404(models.Environment, pk=environment_id)

    form = forms.EnvironmentEditForm(request.POST or None, instance=environment)

    if form.is_valid():
        environment = form.save()
        messages.success(request, _('You successfully updated this environment.'), extra_tags=random.choice(success_messages))
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
    environment = get_object_or_404(models.Environment, pk=environment_id)

    EnvironmentLocationInlineFormSet = \
        inlineformset_factory(
            models.Environment,
            models.EnvironmentLocation,
            fields=('location', 'notes'),
            extra=1,
            widgets={
                'notes': django_forms.Textarea(attrs={'rows': 2})
            }
        )

    formset = EnvironmentLocationInlineFormSet(request.POST or None, instance=environment)

    if formset.is_valid():
        formset.save()
        messages.success(request, _('You successfully updated these locations.'), extra_tags=random.choice(success_messages))
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
    environment = get_object_or_404(models.Environment, pk=environment_id)

    EnvironmentCredentialsInlineFormSet = \
        inlineformset_factory(
            models.Environment,
            models.EnvironmentCredentials,
            fields=('username', 'password', 'role_description', 'notes'),
            extra=1,
            widgets={
                'notes': django_forms.Textarea(attrs={'rows': 2})
            }
        )

    formset = EnvironmentCredentialsInlineFormSet(request.POST or None, instance=environment)

    if formset.is_valid():
        formset.save()
        messages.success(request, _('You successfully updated these credentials.'), extra_tags=random.choice(success_messages))
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
    environment = get_object_or_404(models.Environment, pk=environment_id)

    form = forms.EnvironmentDeleteForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        environment.delete()
        env_type = environment.get_environment_type_display()
        messages.success(request, _('You successfully deleted the "%(env_type)s" environment.') % {'env_type': env_type}, extra_tags=random.choice(success_messages))
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
    engagement = get_object_or_404(models.Engagement, pk=engagement_id)

    pending_activities = engagement.activity_set.filter(status=models.Activity.PENDING_STATUS)
    open_activities = engagement.activity_set.filter(status=models.Activity.OPEN_STATUS)
    closed_activities = engagement.activity_set.filter(status=models.Activity.CLOSED_STATUS)

    status_form = forms.EngagementStatusForm(instance=engagement)

    comment_form = forms.EngagementCommentAddForm()

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
    application = get_object_or_404(models.Application, pk=application_id)

    form = forms.EngagementAddForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        engagement = form.save(commit=False)
        engagement.application = application
        engagement.save()
        messages.success(request, _('You successfully created this engagement.'), extra_tags=random.choice(success_messages))
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
    engagement = get_object_or_404(models.Engagement, pk=engagement_id)

    form = forms.EngagementEditForm(request.POST or None, instance=engagement)

    if request.method == 'POST' and form.is_valid():
        engagement = form.save()
        messages.success(request, _('You successfully updated this engagement.'), extra_tags=random.choice(success_messages))
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
    engagement = get_object_or_404(models.Engagement, pk=engagement_id)

    status_form = forms.EngagementStatusForm(request.POST, instance=engagement)

    if status_form.is_valid():
        engagement = status_form.save()
        eng_status = engagement.get_status_display().lower()
        messages.success(request, _('You successfully updated this engagement\'s status to "%(eng_status)s".') % {'eng_status': eng_status}, extra_tags=random.choice(success_messages))

    return redirect('boh:engagement.detail', engagement_id=engagement.id)


@login_required
@require_http_methods(['POST'])
def engagement_delete(request, engagement_id):
    engagement = get_object_or_404(models.Engagement, pk=engagement_id)

    form = forms.EngagementDeleteForm(request.POST or None)

    if form.is_valid():
        engagement.delete()
        messages.success(request, _('You successfully deleted the engagement.'), extra_tags='Boom!')
        return redirect('boh:application.overview', engagement.application.id)
    else:
        return redirect('boh:engagement.detail', engagement.id)


@login_required
@require_http_methods(['POST'])
def engagement_comment_add(request, engagement_id):
    engagement = get_object_or_404(models.Engagement, pk=engagement_id)

    form = forms.EngagementCommentAddForm(request.POST)

    if form.is_valid():
        comment = form.save(commit=False)
        comment.engagement = engagement
        comment.user = request.user
        comment.save()
        messages.success(request, _('You successfully added a comment to this engagement.'), extra_tags=random.choice(success_messages))
        return redirect(reverse('boh:engagement.detail', kwargs={'engagement_id': engagement.id}) + '#comment-' + str(comment.id))

    return redirect('boh:engagement.detail', engagement_id=engagement.id)


# Activity


@login_required
@require_http_methods(['GET'])
def activity_detail(request, activity_id):
    activity = get_object_or_404(models.Activity, pk=activity_id)

    status_form = forms.ActivityStatusForm(instance=activity)
    comment_form = forms.ActivityCommentAddForm()

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
    engagement = get_object_or_404(models.Engagement, pk=engagement_id)

    form = forms.ActivityAddForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        activity = form.save(commit=False)
        activity.engagement = engagement
        activity.save()
        form.save_m2m()  # https://docs.djangoproject.com/en/1.7/topics/forms/modelforms/#the-save-method
        messages.success(request, _('You successfully added this activity.'), extra_tags=random.choice(success_messages))
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
    activity = get_object_or_404(models.Activity, pk=activity_id)

    form = forms.ActivityEditForm(request.POST or None, instance=activity)

    if request.method == 'POST' and form.is_valid():
        activity = form.save()
        messages.success(request, _('You successfully updated this activity.'), extra_tags=random.choice(success_messages))
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
    activity = get_object_or_404(models.Activity, pk=activity_id)

    status_form = forms.ActivityStatusForm(request.POST, instance=activity)

    if status_form.is_valid():
        activity = status_form.save()
        activity_status = activity.get_status_display().lower()
        messages.success(request, _('You successfully updated this activity\'s status to "%(activity_status)s".') % {'activity_status': activity_status}, extra_tags=random.choice(success_messages))

    return redirect('boh:activity.detail', activity_id=activity.id)


@login_required
@require_http_methods(['POST'])
def activity_delete(request, activity_id):
    activity = get_object_or_404(models.Activity, pk=activity_id)

    form = forms.ActivityDeleteForm(request.POST or None)

    if form.is_valid():
        activity.delete()
        messages.success(request, _('You successfully deleted the activity.'), extra_tags=random.choice(success_messages))
        return redirect('boh:engagement.detail', activity.engagement.id)
    else:
        return redirect('boh:activity.detail', activity.id)


@login_required
@require_http_methods(['POST'])
def activity_comment_add(request, activity_id):
    activity = get_object_or_404(models.Activity, pk=activity_id)

    form = forms.ActivityCommentAddForm(request.POST)

    if form.is_valid():
        comment = form.save(commit=False)
        comment.activity = activity
        comment.user = request.user
        comment.save()
        messages.success(request, _('You successfully added a comment to this activity.'), extra_tags=random.choice(success_messages))
        return redirect(reverse('boh:activity.detail', kwargs={'activity_id': activity.id}) + '#comment-' + str(comment.id))

    return redirect('boh:activity.detail', activity_id=activity.id)


# People

@login_required
@require_http_methods(['GET'])
def person_list(request):
    paginator = Paginator(models.Person.objects.all(), 50)

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
    form = forms.PersonForm(request.POST or None)

    if form.is_valid():
        form.save()
        messages.success(request, _('You successfully created this person.'), extra_tags=random.choice(success_messages))
        return redirect('boh:person.list')

    return render(request, 'boh/person/add.html', {
        'form': form,
        'active_top': 'people'
    })


@login_required
@require_http_methods(['GET'])
def person_detail(request, person_id):
    person = get_object_or_404(models.Person, pk=person_id)

    return render(request, 'boh/person/detail.html', {
        'person': person,
        'active_top': 'people'
    })


@login_required
@require_http_methods(['GET', 'POST'])
def person_edit(request, person_id):
    person = get_object_or_404(models.Person, pk=person_id)
    name = person.first_name + ' ' + person.last_name

    form = forms.PersonForm(request.POST or None, instance=person)

    if request.method == 'POST':
        if form.is_valid():
            person = form.save()
            messages.success(request, _('You successfully updated "%(name)s".') % {'name': name}, extra_tags=random.choice(success_messages))
            return redirect('boh:person.detail', person.id)
        else:
            messages.error(request, _('There was a problem updating "%(name)s".') % {'name': name}, extra_tags=random.choice(error_messages))

    return render(request, 'boh/person/edit.html', {
        'person': person,
        'form': form,
        'active_top': 'people'
    })


@login_required
@require_http_methods(['POST'])
def person_delete(request, person_id):
    person = get_object_or_404(models.Person, pk=person_id)
    name = person.first_name + ' ' + person.last_name

    form = forms.PersonDeleteForm(request.POST or None)

    if form.is_valid():
        person.delete()
        messages.success(request, _('You successfully deleted "%(name)s".') % {'name': name}, extra_tags=random.choice(success_messages))
        return redirect('boh:person.list')
    else:
        return redirect('boh:person.detail', person.id)
