from rest_framework import serializers
from .models import Channel, Category
from rest_framework.reverse import reverse


class ChannelSerializer(serializers.HyperlinkedModelSerializer):
    categories = serializers.HyperlinkedRelatedField(many=True, view_name='category-detail', read_only=True, lookup_field='uuid')
    url = serializers.HyperlinkedIdentityField(view_name='channel-detail', lookup_field='name')
    class Meta:
        model = Channel
        fields = ('uuid', 'name', 'categories', 'url')


class CategorySerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='category-detail', lookup_field='uuid')
    channel = serializers.HyperlinkedRelatedField(view_name='channel-detail', lookup_field='name', queryset=Channel.objects.all() )
    parent = serializers.HyperlinkedRelatedField(view_name='category-detail', lookup_field='uuid', queryset=Category.objects.all() )


    class Meta:
        model = Category
        fields = ('uuid', 'channel', 'name', 'parent', 'url' )
