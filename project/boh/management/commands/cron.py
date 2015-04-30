from django.core.management.base import BaseCommand, CommandError

from boh.connectors.threadfix import ThreadFixAPI


class Command(BaseCommand):

    help = ''

    def handle(self, *args, **options):
        pass