import csv

from django.core.management.base import BaseCommand, CommandError

from  core import Channel, Category


class Command(BaseCommand):
    help = 'Create CSV file from database'


    def add_arguments(self, parser):

        # Positional arguments
        parser.add_argument('channel',  type=str)

    def handle(self, *args, **options):

        channel = options['channel']
        filename = channel+'.csv'

        chn = Channel.objects.filter(name=channel)

        if len(chn)<1:
            raise CommandError("Channel name does not exist.")

        categories = Category.objects.filter(channel=chn)

        with open(filename, 'w') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=['category', 'parent'])
            writer.writeheader()
            for category in categories:
                parent_name = 'Null' if category.parent is None else category.parent.name
                par = {'category': category.name, 'parent': parent_name}
                writer.writerow(par)