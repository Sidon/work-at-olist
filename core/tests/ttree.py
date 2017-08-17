from django.test import TestCase

from core import Channel, Category

ch = 'Shoptest'


class ChannelTestCase(TestCase):
    """
    Class to tests the model Channel
    """
    channel = Channel.objects.create(name=ch)
    def test_models1(self):
        """
        Set up all the tests
        """
        ch_id = self.channel.id
        for node in tree:
            parent_name = node[1] if node[0]!=node[1] else None
            parent = Category.objects.filter(name=parent_name)[0].id if parent_name else None
            # self.dict1[node[0]] =  parent_name

            categ = CategoryFactory(
                name = node[0],
                channel_id=ch_id,
                parent_id = parent,
                parent__parent__parent__parent=None,

            )
            try:
                categ.save()
            except Exception as e:
                print(e)
