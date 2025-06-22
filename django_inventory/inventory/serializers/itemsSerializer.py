from users.models import CustomUser
from rest_framework import serializers
from inventory.models import *
from inventory.serializers.categorySerializer import categorySerializer, subcategorySerializer
from inventory.serializers.locationSerializer import locationSerializer
from datetime import datetime
from django.utils import timezone

class getitemsSerializer(serializers.ModelSerializer):
    category = categorySerializer()
    subcategory =  subcategorySerializer()
    count = serializers.SerializerMethodField()
    locations = serializers.PrimaryKeyRelatedField(many=True, queryset=Locations.objects.all())
    formatted_time = serializers.SerializerMethodField()

    def get_formatted_time(self, obj):
        formatted_time = obj.added_on.astimezone(timezone.get_current_timezone())
        return formatted_time.strftime('%d %B %Y %I:%M %p')

    def to_representation(self, instance):
        data = super().to_representation(instance)
        image_url = self.context['request'].build_absolute_uri(instance.image.url) if instance.image else None
        data['image_url'] = image_url
        # data['formatted_time'] = self.get_formatted_time(instance)
        return data

    def get_count(self, obj):
        items = Items.objects.filter(category = obj.category, subcategory = obj.subcategory)
        return items.count()

    class Meta:
        model = Items
        fields = '__all__'
    
class postitemsSerializer(serializers.ModelSerializer):
    count = serializers.SerializerMethodField()

    class Meta:
        model = Items
        fields = '__all__'
    
    def get_count(self, obj):
        catid = self.context.get('catid')
        items = Items.objects.filter(category = catid)
        return items.count()
    
class updateItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Items
        fields = '__all__'