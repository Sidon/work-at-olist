from django.core.management.base import BaseCommand, CommandError
from  apps.core.models import Channel, Category
import json


class Command(BaseCommand):
    help = 'Create json file from database'

    def handle(self, *args, **options):
        chns = Channel.objects.all()
        for chn in chns:
            nodes = []
            fname = chn.name+'.json'
            categories = Category.objects.filter(channel=chn)
            for category in categories:
                parent_name = 'Null' if category.parent is None else category.parent.name
                nodes.append([category.name, parent_name])
                #chdict[category.name] = {'Parent': parent_name }
            with open(fname, 'w') as fp:
                json.dump(dict(nodes), fp)
