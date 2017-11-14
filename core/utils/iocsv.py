import csv
import os

from  core.models import Channel, Category

def imp_csv(filename, channelname):
    if not os.path.isfile(filename):
        return False

    channel = None if not Channel.objects.filter(name=channelname).exists() else Channel.objects.get(name=channelname)

    # If Channels exists, delete all channel'templates categories
    if channel:
        Category.objects.filter(channel=channel).delete()
    else:
        channel = Channel.objects.create(name=channelname)

    # Save 'root' categories on list and nodes on a list of tuples
    categs = {}
    branches, nodes = [], []
    with open(filename, 'r') as csv_file:
        csv_reader = csv.DictReader(csv_file, delimiter=',')
        for row in csv_reader:
            if row['parent'] in ['Null', 'null','None']:
                branches.append(row['category'])
                categs[row['category']] = row['category']
            else:
                nodes.append([row['category'], row['parent']])
                categs[row['category']] = row['parent']

    # Check for orphans categories
    orphans = [orphan for orphan in categs if categs[orphan] not in categs.keys()]

    if len(orphans)>0:
        print ('CSV Error, categories orphans: ', orphans)
        return (False,orphans)

    # Save branches on database
    for b in branches:
        Category.objects.create(channel=channel, name=b)

    # Save nodes on database
    while nodes:
        for node in nodes:
            parent = None if not Category.objects.filter(name=node[1], channel=channel).exists() else \
                Category.objects.filter(name=node[1])[0]
            if parent:
                Category.objects.create(channel=channel, name=node[0], parent=parent)
                nodes.remove(node)

    return (True, [])

