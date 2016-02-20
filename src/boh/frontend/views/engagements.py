from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render

from boh.core.engagements.models import Engagement


@login_required
def list(request):
    engagements = Engagement.objects.all()

    return render(request, 'frontend/engagements/list.html', {
        'engagements': engagements
    })
