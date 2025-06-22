from django.db import models
from .itemModel import Items
from .locationModel import Locations
from django.db.models.signals import post_save
from django.dispatch import receiver

class Warehouse(models.Model):
    location = models.ForeignKey(Locations, on_delete=models.CASCADE)
    item = models.ForeignKey(Items, on_delete=models.CASCADE)
    added_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'Warehouse'

# @receiver(post_save, sender=Items)
# def create_warehouse_entry(sender, instance, created, **kwargs):
#     if created:
#         # Create a new Warehouse entry
#         for location in instance.location.all():
#             print(location)
#             Warehouse.objects.create(item=instance, location=location)