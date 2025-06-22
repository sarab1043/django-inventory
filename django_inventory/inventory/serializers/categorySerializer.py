from users.models import CustomUser
from rest_framework import serializers
from inventory.models import *
from django.forms.models import model_to_dict
from inventory.models.itemModel import *

import json

class categorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Categories
        fields = '__all__'

class subcategorySerializer(serializers.ModelSerializer):
    # category = serializers.SerializerMethodField()

    class Meta:
        model = Subcategories
        fields = '__all__'

class getsubcategorySerializer(serializers.ModelSerializer):
    subcategory = serializers.SerializerMethodField()

    class Meta:
        model = Categories
        fields = '__all__'
    
    def get_subcategory(self, obj):
        subcategory_obj  = Subcategories.objects.filter(category_id = obj.id)
        subcategory = subcategorySerializer(instance = subcategory_obj, many=True).data
        return subcategory
