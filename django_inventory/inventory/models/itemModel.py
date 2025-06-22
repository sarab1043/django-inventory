from django.db import models
from .categoryModel import *
from .locationModel import *
# from django.contrib.auth.models import User
from users.models import CustomUser
from django.db.models.signals import pre_save
from django.dispatch import receiver
import uuid
import random
import string
from django.db.models.signals import post_save

# Create your models here.

# class Items(models.Model):
#     name = models.CharField(max_length=255)
#     image = models.ImageField(upload_to ='items/', default=None, null=True, blank=True)
#     SKU_number = models.CharField(max_length = 255, unique=True, default=None, blank=True, null=True)
#     category = models.ForeignKey(Categories, on_delete = models.CASCADE)
#     subcategory = models.ForeignKey(Subcategories, on_delete = models.CASCADE, null=True, blank = True)
#     weight = models.FloatField(default=0, null=True, blank=True)
#     price = models.FloatField()
#     location = models.ForeignKey(Locations, on_delete = models.CASCADE, default=None, null=True, blank=True)
#     discounted_price = models.FloatField(blank=True, null=True, default=None)
#     is_available = models.BooleanField(default=True)
#     quantity = models.IntegerField(default=1)
#     created_by = models.ForeignKey(CustomUser, on_delete = models.PROTECT, related_name = "created", null=True, blank=True)
#     updated_by = models.ForeignKey(CustomUser, on_delete = models.PROTECT, related_name = "updated", default = None, null=True, blank=True)
#     added_on = models.DateTimeField(auto_now_add=True)
#     updated_on = models.DateTimeField(auto_now=True)
#     returned = models.BooleanField(default=False)

#     def count(self):
#         count = Items.objects.filter(category=self.category, subcategory=self.subcategory).count()
#         return count

#     def __str__(self):
#         return self.name

#     # def save(self, *args, **kwargs):
#     #     print(self.name)
#     #     print(self.location)

#     class Meta:
#         verbose_name_plural = 'Items'

# @receiver(pre_save, sender=Items)
# def generate_sku(sender, instance, **kwargs):
#     if not instance.SKU_number:
#         # Generate a new SKU number
#         name = instance.name
#         price = instance.price
#         sku = generate_unique_sku(name, price)
#         instance.SKU_number = sku

# def generate_unique_sku(name, price):
#     characters = string.ascii_letters + string.digits
#     code = ''.join(random.choice(characters) for _ in range(5))
#     first_word = name.split()[0]
#     sku = f'{first_word}-{code}'
#     return sku

# @receiver(post_save, sender=Items)
# def add_entry_to_warehouse(sender, instance, created, **kwargs):
#     from .warehouseModel import Warehouse
#     if created:
#         item_obj = Items.objects.get(id = instance.id)
#         print("item", item_obj)
#         loc_obj = Locations.objects.get(name = instance.location)
#         print(loc_obj.id, "locations")

#         save_warehouse = Warehouse.objects.create(item = item_obj, location = loc_obj)
        



class Items(models.Model):
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to ='items/', default=None, null=True, blank=True)
    SKU_number = models.CharField(max_length = 255,  default=None)
    description = models.TextField(default=None, null=True, blank=True)
    ingredients = models.TextField(default=None, null=True, blank=True)
    category = models.ForeignKey(Categories, on_delete = models.CASCADE)
    subcategory = models.ForeignKey(Subcategories, on_delete = models.CASCADE, null=True, blank = True)
    weight = models.FloatField(default=0, null=True, blank=True)
    price = models.FloatField()
    locations = models.ManyToManyField(Locations)
    # location = models.ForeignKey(Locations, on_delete = models.CASCADE, default=None, null=True, blank=True)
    discounted_price = models.FloatField(blank=True, null=True, default=None)
    is_available = models.BooleanField(default=True)
    quantity = models.IntegerField(default=1)
    created_by = models.ForeignKey(CustomUser, on_delete = models.PROTECT, related_name = "created", null=True, blank=True)
    updated_by = models.ForeignKey(CustomUser, on_delete = models.PROTECT, related_name = "updated", default = None, null=True, blank=True)
    added_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def count(self):
        count = Items.objects.filter(category=self.category, subcategory=self.subcategory).count()
        return count

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Items'
    
    def save(self, *args, **kwargs):
        if self.quantity < 0:
            self.quantity = 0
        super().save(*args, **kwargs)