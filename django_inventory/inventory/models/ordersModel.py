from django.db import models
from .itemModel import *
from users.models import CustomUser
from .locationModel import Locations
import uuid
from users.models import UserAddress
# Create your models here.
from django.db.models import F, Max
from datetime import date
from django.utils import timezone
import random

class Orders(models.Model):
    PAYMENT_CHOICES = (
        ('Cash on delivery', 'Cash On Delivery'),
        ('Credit Card', 'Credit Card'),
        ('Debit Card', 'Debit Card'),
        ('PayPal', 'PayPal'),
    )

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=255, default=None, null=True, blank=True)
    product = models.ForeignKey(Items, on_delete=models.CASCADE)
    dispatched_from = models.ForeignKey(Locations, on_delete=models.CASCADE, default=None, null=True, blank=True)
    address = models.ForeignKey(UserAddress, on_delete=models.CASCADE, default=None)
    quantity = models.IntegerField(default=1)
    order_id = models.CharField(max_length=32, unique=True, db_index=True, null=True, blank=True)
    ordered_date = models.DateTimeField(auto_now_add=True)
    confirmed = models.BooleanField(default=True)
    cancelled = models.BooleanField(default=False)
    dispatched = models.BooleanField(default=False)
    delivered = models.BooleanField(default=False)
    returned = models.BooleanField(default=False)
    total_amount = models.IntegerField(default=0, null=True, blank=True)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_CHOICES, default=None, blank=True, null=True)
    delivered_on = models.DateTimeField(default=None, null=True, blank=True)
    cancelled_on = models.DateTimeField(default=None,null=True, blank=True)
    dispatched_on = models.DateField(default=None, null=True, blank=True)

    def save(self, *args, **kwargs):
        self.total_amount = self.quantity * self.product.price

        if self.delivered:
            self.delivered_on = timezone.now()
            self.cancelled = False
            self.dispatched = False
            self.confirmed = False
        elif self.dispatched:
            self.dispatched_on = timezone.now()
            self.cancelled = False
            self.delivered = False
            self.confirmed = False
            self.returned = False
           
            item_update = Items.objects.filter(id = self.product.id).update(quantity=F('quantity') - self.quantity, is_available=False)
            
            item_obj = Items.objects.get(id = self.product.id)
            if (item_obj.quantity < 0):
                Items.objects.filter(id = self.product.id).update(quantity=0)

        elif self.cancelled:
            self.cancelled_on = timezone.now()
            self.dispatched = False
            self.delivered = False
            self.confirmed = False
            self.returned = False
        elif self.returned:
            self.dispatched = False
            self.confirmed = False
            self.cancelled = False

        if not self.order_id:
            self.order_id = uuid.uuid4().hex
        super().save(*args, **kwargs)

    class Meta:
        verbose_name_plural = 'Orders'


class OrderTrack(models.Model):
    STATUS_CHOICES = (
        ('Processing', 'Processing'),
        ('Dispatched', 'Dispatched'),
        ('Delivered', 'Delivered'),
        ('Cancelled', 'Cancelled'),
        ('Returned', 'Returned'),
    )
    tracking_number =  models.CharField(max_length=32, unique=True, null=True, blank=True)
    order = models.ForeignKey(Orders, on_delete=models.CASCADE)
    dispatched_from = models.ForeignKey(Locations, on_delete=models.CASCADE, default=None)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    timestamp = models.DateTimeField(auto_now_add=True)
    expected_delivery_indays = models.IntegerField(default=0)


    def __str__(self):
        return f"Order: {self.order.order_id} - Status: {self.status}"
    
    def save(self, *args, **kwargs):
        if not self.tracking_number:
            self.tracking_number = self.generate_order_tracking_number()
        super().save(*args, **kwargs)

    def generate_order_tracking_number():
        prefix = str(random.randint(100, 999))  
        unique_id = str(uuid.uuid4().int)[:9]  
        tracking_number = f"{prefix}{unique_id}"
        return tracking_number