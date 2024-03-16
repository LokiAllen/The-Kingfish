from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

# Create your models here.
class Shop(models.Model):
    """
     * Stores all currently available shop items
     *
     * @author Jasper
    """
    name = models.TextField()
    description = models.TextField()
    price = models.IntegerField()
    item_id = models.PositiveIntegerField()
    item_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    item_object = GenericForeignKey('item_type', 'item_id')

    class Meta:
        db_table = 'shop'