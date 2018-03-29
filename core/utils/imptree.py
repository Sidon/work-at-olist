import csv
import os

from  core.models import Channel, Category

def imp_tree(filename, channelname):

    if not os.path.isfile(filename):
        return False

    channel = None if not Channel.objects.filter(name=channelname).exists() else Channel.objects.get(name=channelname)

    # If Channels exists, delete all channel'templates categories
    if channel:
        Category.objects.filter(channel=channel).delete()
    else:
        channel = Channel.objects.create(name=channelname)

    f = open(filename, mode='r')
    lines = f.readlines()
    del lines[0]
    lines = [line.rstrip().split(' / ') for line in lines if line != '\n']
    reversed_lines = [line[::-1] for line in lines if line != ['']]
    data_tree = {}

    # Parse txt file
    for line in reversed_lines:
        if len(line) < 2:
            branche = line[0]
            category = (line[0], 'null')
            data_tree[branche] = {'parents': [], 'children': []}
        elif len(line) == 2:
            data_tree[branche]['parents'].append(line[0])
        else:
            for i in range(len(line) - 1):
                category = (line[i].rstrip(','), line[i + 1].rstrip(','))
                if category not in data_tree[branche]['children'] and category[1] != branche:
                    data_tree[branche]['children'].append(category)

    # Bulding tree
    tree = OrderedDict()
    for branche in data_tree:
        tree[branche] = OrderedDict()
        for node in data_tree[branche]['parents']:
            tree[branche][node] = []
            for child in data_tree[branche]['children']:
                if child[1] == node:
                    tree[branche][node].append(child[0])


    # Save to database
    for branche in tree:
        pass


    '''
    for branche in  data_tree:
       current = Category.objects.create(channel=channel, name=branche)
       # Save parents of this branche

       for node in data_tree[branche]['parents']:
           Category.objects.create(channel=channel, name=node, parent=current)

       for child in data_tree[branche]['children']:
           family = current.get_family()
           if child[0] not in data_tree[branche]['parents']:

               try:
                   parent = family.get(name=child[1])
                   Category.objects.create(channel=channel, name=child[0], parent=parent)
               except Exception as e:
                   print (e, child[1])
                   print (family)
    '''