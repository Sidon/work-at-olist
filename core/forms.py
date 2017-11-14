import django_filters
from .models import Channel, Category


class ChannelFilter(django_filters.FilterSet):

    class Meta:
        model = Channel
        fields = ('name',)


class CategoryFilter(django_filters.FilterSet):
    class Meta:
        model = Category
        fields = ('name',)

