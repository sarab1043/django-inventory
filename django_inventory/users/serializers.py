# from django.contrib.auth.models import User
from users.models import CustomUser
from rest_framework import serializers

from.models import CustomUser
from.models import UserAddress

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'email')

class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})
    confirm_password = serializers.CharField(style={'input_type':'password'},write_only=True)

    class Meta:
        model = CustomUser
        fields = ("email", "first_name", "last_name", "password", "confirm_password")

    def validate(self,attrs):
        password = attrs.get('password')
        confirm_password = attrs.get('confirm_password')
        if password != confirm_password:
            raise serializers.ValidationError("password should be matched with confirm_password")
        return attrs
    
    def create(self, validated_data):
        user = CustomUser.objects.create(email=validated_data['email'], first_name=validated_data['first_name'], last_name=validated_data['last_name'])
        user.set_password(validated_data['password'])
        user.save()
        return user

class UserLoginSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = ("email", "first_name", "last_name",)



class UserAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAddress
        fields = '__all__'

class UserProfileSerializer(serializers.ModelSerializer):
    address = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        exclude = ('password',)
    
    def get_address(self, obj):
        user_address = UserAddress.objects.filter(user=obj).first()
        if user_address:
            return UserAddressSerializer(user_address).data
        return None