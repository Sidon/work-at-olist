import uuid
from django.db import models
from mptt.models import MPTTModel, TreeForeignKey


class Channel(models.Model):
    """
    The field "uuid" is the unique handle for each channel, each channel has a friendly identification 
    field called "name". For security reasons the Django autofield is avoided for primary key
    """

    # id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Category(MPTTModel):
    """
    The field "uuid" is  the unique handle for each category, each category has a friendly
    identification field called "name".
    chanell = A category belogns a channel
    parent = A category can have a parent
    """
    #id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)

    name = models.CharField(max_length=100)
    channel = models.ForeignKey(Channel, related_name='categories', on_delete=models.CASCADE)
    #parent = models.ForeignKey('self', null=True, related_name='children', related_query_name='child')
    parent = TreeForeignKey('self', null=True, blank=True,
                            related_name='children', db_index=True)




    def __str__(self):
        return self.name

    def subcategories(self):
        return self.children.all()

