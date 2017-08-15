from . import views
from rest_framework import serializers
from django.core.exceptions import ObjectDoesNotExist
from .models import Channel, Category
from rest_framework.reverse import reverse


# http://www.django-rest-framework.org/api-guide/relations/#custom-relational-fields

class RecursiveField(serializers.BaseSerializer):

    def to_representation(self, value):
        ParentSerializer = self.parent.parent.__class__
        serializer = ParentSerializer(value, context=self.context)
        data = serializer.data
        #data['parent'] = value.parent.uuid
        data['parent'] = value.parent.name
        data['channel'] = value.channel.name
        return data

    def to_internal_value(self, data):
        ParentSerializer = self.parent.parent.__class__
        Model = ParentSerializer.Meta.model
        try:
            instance = Model.objects.get(pk=data)
        except ObjectDoesNotExist:
            raise serializers.ValidationError(
                "Object {0} not found".format(
                    Model().__class__.__name__
                )
            )
        return instance



class CategorySerializer(serializers.ModelSerializer):
    subcategories = RecursiveField(source="children", many=True)
    parent = serializers.SerializerMethodField()
    channel = serializers.SerializerMethodField()
    instance = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ('name', 'uuid', 'parent','channel', 'instance', 'subcategories' )


    def get_parent(self, obj):
        rtrn='null'
        if obj.parent:
            request = self.context['request']
            rtrn = obj.parent.name+': '+reverse('category-detail', kwargs={'uuid': obj.parent.uuid}, request=request)
        return rtrn



    def get_channel(self, obj):
        return obj.channel.name


    def get_instance(self, obj):
        request = self.context['request']
        return reverse('category-detail', kwargs={'uuid': obj.uuid}, request=request)


class ChannelSerializer(serializers.ModelSerializer):
    categories = CategorySerializer(many=True)
    instance = serializers.SerializerMethodField()

    class Meta:
        model = Channel
        fields = ('uuid', 'name', 'instance', 'categories')

    def get_instance(self, obj):
        request = self.context['request']
        return  reverse('channel-detail', kwargs={'name': obj.name}, request=request)


