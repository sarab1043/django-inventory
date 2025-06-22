from django.contrib import admin
from inventory.models.itemModel import Items
from inventory.models.categoryModel import Categories, Subcategories
from inventory.models.locationModel import Locations
from inventory.models.ordersModel import Orders, OrderTrack
from inventory.models.warehouseModel import *

class ItemsAdmin(admin.ModelAdmin):
    list_display = ['id', 'SKU_number', 'name', 'category', 'subcategory', 'quantity']

class CategoriesAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']

class SubcategoriesAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']

class LocationsAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']

class OrdersAdmin(admin.ModelAdmin):
    list_display = ['id']



admin.site.register(Items, ItemsAdmin)
admin.site.register(Categories, CategoriesAdmin)
admin.site.register(Subcategories, SubcategoriesAdmin)
admin.site.register(Locations, LocationsAdmin)
admin.site.register(Orders, OrdersAdmin)
admin.site.register(Warehouse)
admin.site.register(OrderTrack)