from users.models import CustomUser
from rest_framework import serializers
from inventory.models import *
from inventory.serializers.itemsSerializer import getitemsSerializer
from inventory.serializers.categorySerializer import categorySerializer, subcategorySerializer
from inventory.serializers.locationSerializer import locationSerializer
from users.serializers import UserAddressSerializer,UserSerializer
from django.utils import timezone

class getOrdersSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    product = getitemsSerializer()
    dispatched_from = locationSerializer()
    address = UserAddressSerializer()
    confirmed_on = serializers.SerializerMethodField()
    cancelled_on = serializers.SerializerMethodField()
    delivered_on = serializers.SerializerMethodField()

    def get_confirmed_on(self, obj):
        confirmed_on = obj.ordered_date.astimezone(timezone.get_current_timezone())
        return confirmed_on.strftime('%d %B %Y %I:%M %p')

    def get_cancelled_on(self, obj):
        if obj.cancelled_on:
            cancelled_on = obj.cancelled_on.astimezone(timezone.get_current_timezone())
            return cancelled_on.strftime('%d %B %Y %I:%M %p')
        else:
            return None

    def get_delivered_on(self, obj):
        if obj.delivered_on:
            delivered_on = obj.delivered_on.astimezone(timezone.get_current_timezone())
            return delivered_on.strftime('%d %B %Y %I:%M %p')
        else:
            return None
    class Meta:
        model = Orders
        fields = '__all__'

class updateOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Orders
        fields = ('cancelled', 'dispatched', 'delivered', 'returned')
    
    
class postOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Orders
        fields = '__all__'