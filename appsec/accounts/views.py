from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_http_methods

from accounts.forms import UserEditForm
from accounts.models import UserProfile

# Create your views here.

@login_required
@require_http_methods(['GET', 'POST'])
def settings_profile(request):

    user_form = UserEditForm(request.POST or None, instance=request.user)

    if request.method == 'POST' and user_form.is_valid():
        user_form.save()
        messages.success(request, 'You successfully updated your profile.', extra_tags='Woot!')

    return render(request, 'accounts/settings/profile.html', {
        'active': 'profile',
        'user_form': user_form
    })


@login_required
@require_http_methods(['GET', 'POST'])
def settings_account_settings(request):



    return render(request, 'accounts/settings/account_settings.html', {
        'active': 'settings'
    })


@login_required
@require_http_methods(['GET', 'POST'])
def settings_notifications(request):

    return render(request, 'accounts/settings/notifications.html', {
        'active': 'notifications'
    })
