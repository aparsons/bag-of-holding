from django.core.management.base import BaseCommand, CommandError

from threadfix_api import threadfix

from ... import models


class Command(BaseCommand):

    help = ''

    def add_arguments(self, parser):
        parser.add_argument('--threadfix', action='store_true', dest='threadfix', default=False, help='')

    def handle(self, *args, **options):
        if options['threadfix']:
            self._threadfix()

    def _threadfix(self):
        applications = models.Application.objects.exclude(threadfix__isnull=True).exclude(threadfix_team_id__isnull=True).exclude(threadfix_application_id__isnull=True)

        for application in applications:
            tf_api = threadfix.ThreadFixAPI(host=application.threadfix.host, api_key=application.threadfix.api_key, verify_ssl=application.threadfix.verify_ssl)

            response = tf_api.get_application(application_id=application.threadfix_application_id)
            if response.success:
                print(response.data_json())
                critical_count = response.data['criticalVulnCount']
                high_count = response.data['highVulnCount']
                medium_count = response.data['mediumVulnCount']
                low_count = response.data['lowVulnCount']
                informational_count = response.data['infoVulnCount']

                models.ThreadFixMetrics.objects.create(
                    application=application,
                    critical_count=critical_count,
                    high_count=high_count,
                    medium_count=medium_count,
                    low_count=low_count,
                    informational_count=informational_count
                ).save()
            else:
                print('An error occurred: ' + response.message)
