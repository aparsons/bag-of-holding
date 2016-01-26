from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render

from boh.core.applications.models import Application


@login_required
def list(request):
    applications = Application.objects.all()

    return render(request, 'frontend/applications/list.html', {
        'applications': applications
    })


@login_required
def overview(request, application_id):
    application = get_object_or_404(Application, pk=application_id)

    # Experimental
    #activity_feed = Application.objects.activity_feed(application)
    activity_feed = application.activity_feed()

    return render(request, 'frontend/applications/overview.html', {
        'application': application,
        'activity_feed': activity_feed
    })


@login_required
def engagements(request, application_id):
    pass


@login_required
def benchmarks(request, application_id):
    application = get_object_or_404(Application, pk=application_id)

    return render(request, 'frontend/applications/benchmarks.html', {
        'application': application
    })
