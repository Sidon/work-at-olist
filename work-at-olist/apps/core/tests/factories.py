import factory
import uuid
from apps.core.models import Channel, Category


class ChannelFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Channel


# https://github.com/FactoryBoy/factory_boy/issues/173
class CategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Category

    parent = factory.SubFactory('apps.core.tests.factories.CategoryFactory')
    channel_id=uuid.uuid4()
