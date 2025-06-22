from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User 
from django.contrib.auth import login, logout, authenticate
from django.shortcuts import redirect, reverse
from django.views.generic import TemplateView
from users.serializers import *
# from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView
from rest_framework.renderers import JSONRenderer
from django.http import JsonResponse
from rest_framework import status
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_protect
from django.middleware.csrf import get_token
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken
import jwt
from rest_framework_simplejwt.authentication import JWTAuthentication
from django_inventory import settings
from rest_framework_simplejwt.tokens import UntypedToken
import base64
from rest_framework.authtoken.models import Token
from rest_framework import authentication, permissions
from inventory.models import Orders
from inventory.serializers.orderSerializer import *

class RegisterView(APIView):
    def post(self, request, format=None ):
        email = request.data['email']
        first_name = request.data['first_name']
        last_name = request.data['last_name']
        password = request.data['password']
        confirm_password = request.data['confirm_password']
        already_exists = CustomUser.objects.filter(email = email)
        if already_exists:
            print("email exists")
            return Response({'error': 'User already exists.'}, status=status.HTTP_400_BAD_REQUEST)
            
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            user = CustomUser.objects.get(email=serializer.data.get('email'))
            # refresh = RefreshToken.for_user(user)
            user_details = serializer.data
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }, status=status.HTTP_201_CREATED)
            return Response({"data": user_details, "status": status.HTTP_200_OK, "success": "User Registered successfully"})
        else:
            return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    def post(self, request, format=None):
        print(request.data)
        
        email = request.data['userName']
        
        password = request.data['password']
        user = authenticate(request, email=email, password=password)
        if user:
            login(request, user)
            user_obj = CustomUser.objects.get(email=email)
            serializer = UserLoginSerializer(user_obj)
            refresh = RefreshToken.for_user(user_obj)
            user_details = serializer.data
            # token, _ = Token.objects.get_or_create(user=user)
            user_details['token'] = str(refresh.access_token)
            
            return Response({"data": user_details, "status": status.HTTP_200_OK, "success": "User Logged In Successfully"})
        else:
            return Response({'error': 'Invalid login credentials.'}, status=status.HTTP_400_BAD_REQUEST)
      
class UserProfileView(APIView):
    # authentication_classes = [authentication.TokenAuthentication]s
    permission_classes = [permissions.IsAuthenticated]
 
    def get(self, request, format=None):
        user = request.user
        if user:
            serializer = UserProfileSerializer(user)
            return Response({"data": serializer.data, "status": status.HTTP_200_OK, "success": "Profile Fetched Successfully"})
        else:
            return Response({'error': 'User Not Found'}, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, format=None):
        user = request.user
        print(request.data)
        if user.is_authenticated:
            serializer = UserProfileSerializer(user, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({"data":serializer.data, "status": status.HTTP_200_OK, "success": "Profile Updated Successfully"})
        else:
            return Response({'error': 'User Not Found'}, status=status.HTTP_400_BAD_REQUEST)

# class UpdateUserProfileView(APIView):
#     authentication_classes = [authentication.TokenAuthentication]
#     permission_classes = [permissions.IsAuthenticated]
 
#     def get(self, request, format=None):
#         user = request.user
#         if user.is_authenticated:
#             serializer = UserProfileSerializer(user, data=request.data, partial=True)
#             if serializer.is_valid():
#                 serializer.save()
#                 return Response({"data":serializer.data, "status": status.HTTP_200_OK, "success": "Profile Updated Successfully"})
#         else:
#             return Response({'error': 'User Not Found'}, status=status.HTTP_400_BAD_REQUEST)

class LogoutView(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):
        user = request.user
        if user:
            request.user.auth_token.delete()
            logout(request)
            return Response({"msg" : "User logged out Successfully"})
        else:
            return Response({'error': 'User Not Found'}, status=status.HTTP_400_BAD_REQUEST)

class UserAddressView(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):
        user = request.user.id
        if user:
            user_address = UserAddress.objects.get(user = user,  default=True)
            if user_address:
                serializer = UserAddressSerializer(user_address)
                return Response({"data": serializer.data, "status": status.HTTP_200_OK, "success": "User Address Fetched Successfully"})
            else:
                return Response({"data": [], "status": status.HTTP_200_OK, "success": "User Address Fetched Successfully"})
        else:
            return Response({'error': 'User Not Found'}, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request, format=None):
        user = request.user
        data = request.data
        try:
            if user.is_authenticated:
                serializer = UserAddressSerializer(data=request.data)
                if serializer.is_valid():
                    serializer.save(user=user)
                    if 'default' in data and data['default'] == True:
                        address = UserAddress.objects.get(id = serializer.data['id'])
                        update_address = UserAddress.objects.filter(user = request.user.id).exclude(id = address.id).update(default=False)
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
                else:
                    return Response({"data": [], "error": serializer.errors, "status": status.HTTP_400_BAD_REQUEST, "success": "Validation Error"})
            else:
                return Response({'error': 'User Not Found'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(e)

    def put(self, request, id, format=None):
            user = request.user
            data = request.data
            if user.is_authenticated:
                try:
                    address = UserAddress.objects.get(id=id)
                    serializer = UserAddressSerializer(address, data=data)
                    if serializer.is_valid():
                        serializer.save()
                        return Response(serializer.data, status=status.HTTP_200_OK)
                    else:
                        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                except UserAddress.DoesNotExist:
                    return Response({"error": "Address not found"}, status=status.HTTP_404_NOT_FOUND)
            else:
                return Response({"error": "User not authenticated"}, status=status.HTTP_401_UNAUTHORIZED)

class UserOrdersView(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):
        if request.user.is_authenticated:
            orders = Orders.objects.filter(user = request.user.id).order_by('-ordered_date')
            serializer = getOrdersSerializer(orders, many=True, context={'request': request})
            return Response({"data": serializer.data, "status": status.HTTP_200_OK, "success": "User's Orders fetched Successfully"})
        else:
            return Response({'error': 'User not found'}, status=status.HTTP_400_BAD_REQUEST)

class GetUserOrderView(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, id, format=None):
        if request.user.is_authenticated:
            try:
                order = Orders.objects.get(id=id, user=request.user.id)
                serializer = getOrdersSerializer(order, context={'request': request})
                return Response({"data": serializer.data, "status": status.HTTP_200_OK, "success": "User's Order fetched Successfully"})
            except Orders.DoesNotExist:
                return Response({'error': 'Order Not Found'}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({'error': 'User Not Found'}, status=status.HTTP_400_BAD_REQUEST)


