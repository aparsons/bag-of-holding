from django.conf import settings
from django.http import HttpResponse
from django.template import loader, Context
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from . import models


class Report(object):
    """Base class used for generating reports."""

    def __init__(self, report_type, file_name, file_format, requester):
        self.report_type = report_type
        self.file_name = file_name
        self.file_format = file_format
        self.requester = requester

        content_types = {
            'csv': 'text/csv',
            'html': 'text/html'
        }

        self.content_type = content_types[file_format]

    def __str__(self):
        return '%s: %s.%s' % (self.report_type, self.file_name, self.file_format)

    def generate(self):
        raise NotImplementedError(_('Subclasses must override generate()'))

    def response(self):
        response = HttpResponse(content_type=self.content_type)
        if not settings.DEBUG:
            response['Content-Disposition'] = 'attachment; filename="%s.%s"' % (self.file_name, self.file_format)
        response.write(self.generate())
        return response


class EngagementCoverageReport(Report):

    def __init__(self, file_name, file_format, organizations, requester):
        super(EngagementCoverageReport, self).__init__(_('Engagement Coverage Report'), file_name, file_format, requester)
        self.organizations = organizations

    def generate(self):
        if not self.organizations:
            self.organizations = models.Organization.objects.all()

        if self.file_format == 'html':
            template = loader.get_template('boh/reports/engagement_coverage.html')
            context = Context({
                'current_datetime': timezone.now(),
                'requester': self.requester,
                'organizations': self.organizations
            })
            return template.render(context)
        else:
            return 'test, test'


class ThreadFixSummaryReport(Report):

    def __init__(self, file_name, file_format, organizations, requester):
        super(ThreadFixSummaryReport, self).__init__(_('ThreadFix Summary Report'), file_name, file_format, requester)
        self.organizations = organizations

    def generate(self):
        if not self.organizations:
            self.organizations = models.Organization.objects.all()

        if self.file_format == 'html':
            template = loader.get_template('boh/reports/threadfix_summary.html')
            context = Context({
                'current_datetime': timezone.now(),
                'requester': self.requester,
                'organizations': self.organizations
            })
            return template.render(context)
        else:
            return 'test, test'


class AppSummaryReport(Report):

    def __init__(self, file_name, file_format, applications, requester):
        super(AppSummaryReport, self).__init__(_('Application Summary Report'), file_name, file_format, requester)
        self.applications = applications

    def generate(self):
        if not self.applications:
            self.applications = models.Application.objects.all()

        if self.file_format == 'html':
            template = loader.get_template('boh/reports/app_summary.html')
            context = Context({
                'current_datetime': timezone.now(),
                'requester': self.requester,
                'applications': self.applications
            })
            return template.render(context)
        else:
            return 'test, test'
