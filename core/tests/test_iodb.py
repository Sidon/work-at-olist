from django.test import TestCase
from core.models import Category, Channel
from core.utils import iocsv


class ImportTestCase(TestCase):
    categs1 = [('categ0', 'categ0'), ('categ01', 'categ0'), ('categ011', 'categ01'), ('categ1', 'categ1'),
               ('categ11', 'categ1'),  ('categ111', 'categ11'), ('categ2', 'categ2'), ('categ21', 'categ2'),
               ('categ211', 'categ21')]

    def test_import(self):
        iocsv.imp_categories('test1.csv', 'Test1')
        channel = Channel.objects.get(name='Test1')
        categories = Category.objects.all().filter(channel=channel)
        categs2 = [(category.name, category.name if not category.parent else category.parent.name) for category in categories]
        self.assertEqual(self.categs1, categs2)


