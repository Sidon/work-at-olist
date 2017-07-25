#Core Django imports
from  apps.core.models import Channel, Category



ch = 'Shoptest'
tree=(('Books','Books'), ('National Literature', 'Books'), ('Science fiction', 'National Literature'),
       ('Fantastic Fiction', 'National Literature'),('Foreign literature', 'Books'), ('Computers', 'Computers'),
       ('Applications', 'Computers'), ('Database', 'Computers'), ('Programming','Computers'), ('Games', 'Games'),
       ('XBOX 360', 'Games'), ('Console', 'XBOX 360'), ('Games', 'XBOX 360'), ('Accessories', 'XBOX 360'),
       ('XBOX One', 'XBOX One'), ('Console','XBOX One'), ('Games', 'XBOX One'), ('Accessories', 'XBOX One'),
       ('Playstation 4', 'Games'),('Computing','Computing'),('Notebooks','Computing'),('Tablets', 'Computing'),
       ('Desktop', 'Computing'))



channel = Channel.objects.create(name='Shoptest')
def create_models():
    """
    Set up all the tests
    """
    for node in tree:
        parent_name = node[1] if node[0]!=node[1] else None
        parent = Category.objects.filter(name=parent_name)[0] if parent_name else None
        category = Category.objects.create(name=node[0], channel=channel)
        if parent:
            category.parent=parent
            category.save()


def list_nodes():
    nodes =  Category.objects.all()
    for node in nodes:
        print(' ')
        pname = 'None' if not node.parent else node.parent.name
        print(node.name, 'Parent: ', pname )
        print('=============')
        for s in node.subcategories():
            print(s.name)



