import os

from django.core.management.base import BaseCommand, CommandError

from core import imp_categories
from workatolist.settings import BASE_DIR


class Command(BaseCommand):
    help = 'read_csv and populate database'
    def add_arguments(self, parser):
        # Positional arguments
        parser.add_argument('filename', type=str)
        parser.add_argument('channelname', type=str)

    def handle(self, *args, **options):
        # make sure file path resolves
        filename = os.path.join(BASE_DIR , options['filename'])
        if not os.path.isfile(filename):
            raise CommandError("File does not exist on project root.")
        imp_categories(filename,options['channelname'])