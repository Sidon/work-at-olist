from rest_framework import serializers
from .models import Channel, Category
from rest_framework.reverse import reverse


class ObjCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('uuid', 'channel', 'name', 'parent' )


class ObjChannelSerializer(serializers.ModelSerializer):
    categories = ObjCategorySerializer(many=True, read_only=True)

    class Meta:
        model = Channel
        fields = ('uuid', 'name', 'categories')



##############################################################



class UrlChannelSerializer(serializers.HyperlinkedModelSerializer):
    categories = serializers.HyperlinkedRelatedField(many=True,
                                                     view_name='url-category-detail',
                                                     read_only=True,
                                                     lookup_field='uuid')

    url = serializers.HyperlinkedIdentityField(view_name='url-channel-detail',
                                               lookup_field='name')
    class Meta:
        model = Channel
        fields = ('uuid', 'name', 'url', 'categories')


class UrlCategorySerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='url-category-detail', lookup_field='uuid')

    channel = serializers.HyperlinkedRelatedField(view_name='url-channel-detail',
                                                  lookup_field='name',
                                                  queryset=Channel.objects.all() )

    parent = serializers.HyperlinkedRelatedField(view_name='url-category-detail',
                                                 lookup_field='uuid',
                                                 queryset=Category.objects.all() )


    class Meta:
        model = Category
        fields = ('uuid', 'channel', 'name', 'parent', 'url' )

