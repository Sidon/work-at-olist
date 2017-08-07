import os
import json
import csv
from django.core.management.base import BaseCommand, CommandError
from  apps.core.models import Channel, Category
from workatolist.settings import BASE_DIR


class Command(BaseCommand):
    help = 'read_csv and populate database'


    def add_arguments(self, parser):

        # Positional arguments
        parser.add_argument('filename', type=str)
        parser.add_argument('channelname', type=str)

    def handle(self, *args, **options):

        # make sure file path resolves

        suffix = '.csv'
        filename = os.path.join(BASE_DIR,options['filename']+suffix)

        if not os.path.isfile(filename):
            raise CommandError("File does not exist on project's root.")

        channel = Channel.objects.filter(name=options['channelname'])[0]

        # If Channels exists, delete all channel's categories
        if channel:
            Category.objects.filter(channel=channel).delete()
        else:
            Channel.objects.create(name=options['channelname'])

        nodes = []
        # Save 'root' categories on database and nodes on lists
        with open(filename, 'r') as csv_file:
            csv_reader = csv.DictReader(csv_file, delimiter=',')
            for row in csv_reader:
                if row['parent']=='Null':
                    Category.objects.create(channel=channel, name=row['category'])
                else:
                    nodes.append([row['category'], row['parent']])

        # Save nodes on database
        while nodes:
            for node in nodes:
                parent = None if not Category.objects.filter(name=node[1]).exists() else \
                    Category.objects.filter(name=node[1])[0]
                if parent:
                    Category.objects.create(channel=channel, name=node[0], parent=parent)
                    nodes.remove(node)
