from django.core.management.base import BaseCommand
from  apps.core.models import Channel, Category


tree1=(('Books','Books'), ('National Literature', 'Books'), ('Science fiction', 'National Literature'),
       ('Fantastic Fiction', 'National Literature'),('Foreign literature', 'Books'), ('Computers', 'Computers'),
       ('Applications', 'Computers'), ('Database', 'Computers'), ('Programming','Computers'), ('Games', 'Games'),
       ('XBOX 360', 'Games'), ('Console', 'XBOX 360'), ('Games', 'XBOX 360'), ('Accessories', 'XBOX 360'),
       ('XBOX One', 'XBOX One'), ('Console','XBOX One'), ('Games', 'XBOX One'), ('Accessories', 'XBOX One'),
       ('Playstation 4', 'Games'),('Computing','Computing'),('Notebooks','Computing'),('Tablets', 'Computing'),
       ('Desktop', 'Computing'))

tree2=(('Books','Books'),('National Literature', 'Books'),('Didatic','Books'),('Fiction','Books'),('Novell','Books'),
       ('Science fiction', 'National Literature'),('Fantastic Fiction', 'National Literature'),
       ('Foreign literature', 'Books'), ('Computers', 'Computers'),('Geography','Didatic'), ('History','Didatic'),
       ('Applications', 'Computers'), ('Database', 'Computers'),
       ('Programming','Computers'),('Mother Board', 'Computers'),('Softwares','Computers'),('Accessories','Computers'),
       ('Games', 'Games'),
       ('XBOX 360', 'Games'), ('Console', 'XBOX 360'), ('Games', 'XBOX 360'), ('Accessories', 'XBOX 360'),
       ('XBOX One', 'XBOX One'), ('Console','XBOX One'), ('Games', 'XBOX One'), ('Accessories', 'XBOX One'),
       ('Playstation 4', 'Games'),('Computing','Computing'),('Notebooks','Computing'),('Tablets', 'Computing'),
       ('Desktop', 'Computing'))


chns = {'Shop1': tree1, 'Shop2': tree2}

print ('aqui')


class Command(BaseCommand):
    help = 'Create initial data'

    def handle(self, *args, **options):

        Category.objects.all().delete()
        Channel.objects.all().delete()

        for chn in chns.keys():
            channel = Channel.objects.create(name=chn)
            for node in chns[chn]:
                parent_name = node[1] if node[0]!=node[1] else None
                parent = Category.objects.filter(name=parent_name)[0] if parent_name else None
                category = Category.objects.create(name=node[0], channel=channel)
                if parent:
                    category.parent=parent
                    category.save()
