
from rest_framework import serializers
from rest_framework.reverse import reverse
from .models import Channel, Category
from rest_framework_tracking.models import APIRequestLog


class ChannelSerializer(serializers.ModelSerializer):
    links = serializers.SerializerMethodField()
    data_face = {}

    class Meta:
        model = Channel
        fields = ('uuid', 'name', 'links')

    def get_links(self, obj):
        request = self.context['request']
        request = {'self': reverse('channel-detail', kwargs={'uuid': obj.uuid}, request=request)}

        if bool(request.POST):
            pass

        return links



# Testing: https://stackoverflow.com/a/35994826/2879341
class CategorySerializer(serializers.ModelSerializer):

    subcategories = serializers.SerializerMethodField(read_only=True, method_name="get_child_categories")
    links = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ('name', 'uuid', 'subcategories', 'links')

    def get_child_categories(self, obj):
        """ self referral field """
        serializer = CategorySerializer(
            instance=obj.subcategories_set.all(),
            many=True
        )
        return serializer.data


    def get_links(self, obj):
        request = self.context['request']
        request = {'self': reverse('channel-detail', kwargs={'uuid': obj.uuid}, request=request)}

        if bool(request.POST):
            pass

        return links


