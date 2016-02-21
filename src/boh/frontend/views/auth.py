from django.conf import settings
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import redirect, render, resolve_url
from django.utils.http import is_safe_url
from django.views.decorators.cache import never_cache


REDIRECT_FIELD_NAME = 'next'


@never_cache
def login(request):
    """Displays the login form and handles the login action."""

    # Ensure the user-originating redirection url is safe.
    redirect_to = request.POST.get(REDIRECT_FIELD_NAME, request.GET.get(REDIRECT_FIELD_NAME, ''))
    if not is_safe_url(url=redirect_to, host=request.get_host()):
        redirect_to = resolve_url(settings.LOGIN_REDIRECT_URL)

    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            auth_login(request, form.get_user())
            return redirect(redirect_to)
    else:
        if request.user.is_authenticated():
            return redirect(redirect_to)

        form = AuthenticationForm(request)
    return render(request, 'frontend/auth/login.html', {
        'form': form,
        REDIRECT_FIELD_NAME: redirect_to,
    })


@never_cache
def logout(request):
    """Logs out the user and displays 'You are logged out' message."""
    auth_logout(request)
    return render(request, 'frontend/auth/logout.html')
