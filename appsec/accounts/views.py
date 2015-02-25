from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_http_methods

from accounts.models import UserProfile

# Create your views here.

@login_required
@require_http_methods(['GET', 'POST'])
def profile_edit(request):

    return render(request, 'accounts/profile/edit.html')
