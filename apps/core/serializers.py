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
        data['parent'] = value.parent.uuid
        data['channel'] = value.channel.name
        return data

    def to_internal_value(self, data):
        ParentSerializer = self.parent.parent.__class__
        Model = ParentSerializer.Meta.model
        try:
            instance = Model.objects.get(pk=data)
        except ObjectDoesNotExist:
            raise serializers.ValidationError(
                "Objeto {0} não encontrado".format(
                    Model().__class__.__name__
                )
            )
        return instance



class ObjCategorySerializer(serializers.ModelSerializer):
    subcategories = RecursiveField(source="children", many=True)
    parent = serializers.SerializerMethodField()
    channel = serializers.SerializerMethodField()
    links = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ('name', 'uuid', 'parent', 'channel', 'links', 'subcategories' )


    def get_parent(self, obj):
        return 'null' if not obj.parent else obj.parent.name

    def get_channel(self, obj):
        return obj.channel.name


    def get_links(self, obj):
        request = self.context['request']
        return {
            'self': reverse('category-detail',
                kwargs={'uuid': obj.uuid}, request=request),
        }




class ObjChannelSerializer(serializers.ModelSerializer):
    categories = ObjCategorySerializer(many=True)
    links = serializers.SerializerMethodField()

    class Meta:
        model = Channel
        fields = ('uuid', 'name', 'links', 'categories')

    def get_links(self, obj):
        request = self.context['request']
        return {
            'self': reverse('channel-detail',
                kwargs={'name': obj.name}, request=request),
        }



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
        fields = ('uuid', 'name', 'url', 'channel', 'parent' )

