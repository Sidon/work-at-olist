from django.core.management.base import BaseCommand, CommandError
from  apps.core.models import Channel, Category
import json


class Command(BaseCommand):
    help = 'read_csv and populate database'


    def add_arguments(self, parser):

        # Positional arguments
        parser.add_argument('filename', type=str)
        parser.add_argument('chn', type=str)

        # Named (optional) arguments
        parser.add_argument('--preserve',
                            action='store_true',
                            dest='preserve',
                            default='False',
                            help='Preserve old records, just update')

    def handle(self, *args, **options):

        # make sure file path resolves
        if not os.path.isfile(options['filename']) :
            raise CommandError("File does not exist at the specified path.")

        filename = options['filename']
        chn = options['chn']
        channel = Channel.objects.filter(name=chn)[0]

        if channel:
            Category.objects.filter(channel=channel.name).delete()

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
