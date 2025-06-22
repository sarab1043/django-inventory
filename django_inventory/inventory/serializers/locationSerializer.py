from users.models import CustomUser
from rest_framework import serializers
from inventory.models import *


class locationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Locations
        fields = "__all__"

class locationItemsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Items
        fields = "__all__"