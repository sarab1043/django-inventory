from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, reverse
from rest_framework.views import APIView
from rest_framework.renderers import JSONRenderer
from django.http import JsonResponse
from rest_framework import status
from rest_framework.response import Response
from rest_framework import authentication, permissions
# from inventory.serializers.itemsSerializer import *
from inventory.serializers.orderSerializer import *
from inventory.models import *
from django.db.models import F

class orderView(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):
        orders = Orders.objects.all().order_by('-ordered_date')
        user = request.user
        if user.is_authenticated:
            if orders:
                serializer = getOrdersSerializer(orders, many=True, context={'request': request})
                return Response({"data": serializer.data, "status": status.HTTP_200_OK, "success": "Orders Fetched Successfully"})
            else:
                return Response({"data": [], "error": status.HTTP_400_BAD_REQUEST, "message": "Orders do not found"})
        else:
            return Response({"data": [], "error": status.HTTP_400_BAD_REQUEST, "message": "User not found"})
    
    def post(self, request, format=None):
        data = request.data
        user = request.user
        if user.is_authenticated:
            item_obj = Items.objects.get(id = data['product'])
            if (item_obj.quantity > 0):
                serializer = postOrderSerializer(data = data)
                if serializer.is_valid():
                    serializer.save(user=request.user)
                    return Response({"data": serializer.data, "status": status.HTTP_201_CREATED, "success": "Orders Placed Successfully"})
                else:
                    return Response({"data": [], "error": serializer.errors, "status": status.HTTP_400_BAD_REQUEST, "success": "Validation Error"})
            else:
                return Response({"data": [], "error": status.HTTP_400_BAD_REQUEST, "message": "Item out of stock"})
        else:
            return Response({"data": [], "error": status.HTTP_400_BAD_REQUEST, "message": "User not found"})

    def put(self, request, id, format=None):
        try:
            data = request.data
            order_obj = Orders.objects.get(id = id)
            if 'cancelled' in data and data['cancelled'] == True:
                if (order_obj.delivered == False):
                    order_obj.dispatched = False 
                    order_obj.save()
                else:
                    return Response({'error': "This Order cant'be be cancelled."}, status=status.HTTP_400_BAD_REQUEST)

            if 'delivered' in data or 'dispatched' in data:
                if order_obj.cancelled == True:
                    return Response({'error': 'Order already cancelled.'}, status = status.HTTP_400_BAD_REQUEST)
            
            if 'dispatched' in data:
                if order_obj.delivered == True:
                    return Response({"error": "Order already delivered"}, status = status.HTTP_400_BAD_REQUEST)
            
            if 'returned' in data:
                if order_obj.delivered == False:
                    return Response({"error": "Order not delivered yet"}, status = status.HTTP_400_BAD_REQUEST)

            serializer = updateOrderSerializer(order_obj, data=data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({"data": serializer.data, "status": status.HTTP_200_OK, "message": "Order  Updated Successfully"})
            else:
               return Response({"error": "Something went wrong"}, status = status.HTTP_400_BAD_REQUEST)
        except Items.DoesNotExist:
            return Response({"error": "Order do not found"}, status= status.HTTP_400_BAD_REQUEST)
    
class cancelledOrderView(APIView):
    def get(self, request, format=None):
        order_obj = Orders.objects.filter(cancelled=True).order_by('-added_on')
        if order_obj:
            serializer = getOrdersSerializer(order_obj, many=True, context={'request': request})
            return Response({"data": serializer.data, "status": status.HTTP_200_OK, "success": "Orders Fetched Successfully"})
        else:
            return Response({"data": [], "status": status.HTTP_400_BAD_REQUEST, "message": "Orders do not found"})

class dispatchedOrderView(APIView):
    def get(self, request, format=None):
        order_obj = Orders.objects.filter(dispatched=True).order_by('-added_on')
        if order_obj:
            serializer = getOrdersSerializer(order_obj, many=True, context={'request': request})
            return Response({"data": serializer.data, "status": status.HTTP_200_OK, "success": "Orders Fetched Successfully"})
        else:
            return Response({"data": [], "status": status.HTTP_400_BAD_REQUEST, "message": "Orders do not found"})

class deliveredOrderView(APIView):
    def get(self, request, format=None):
        order_obj = Orders.objects.filter(delivered=True).order_by('-added_on')
        if order_obj:
            serializer = getOrdersSerializer(order_obj, many=True, context={'request': request})
            return Response({"data": serializer.data, "status": status.HTTP_200_OK, "success": "Orders Fetched Successfully"})
        else:
            return Response({"data": [], "status": status.HTTP_400_BAD_REQUEST, "message": "Orders do not found"})

class getOrderView(APIView):
    def get(self, request, id, format=None):
        order_obj = Orders.objects.filter(id = id).first()
        if order_obj:
            serializer = getOrdersSerializer(order_obj, context={'request' : request})
            return Response({"data": serializer.data, "status": status.HTTP_200_OK, "success": "Order Fetched Successfully"})
        else:
            return Response({"data": [], "status": status.HTTP_400_BAD_REQUEST, "message": "Order do not found"})

class confirmedOrderView(APIView):
    def get(self, request, format=None):
        order_obj = Orders.objects.filter(confirmed=True)
        if order_obj:
            serializer = getOrdersSerializer(order_obj, many=True, context={'request': request})
            return Response({"data": serializer.data, "status": status.HTTP_200_OK, "success": "Orders Fetched Successfully"})
        else:
            return Response({"data": [], "status": status.HTTP_400_BAD_REQUEST, "message": "Orders do not found"})

class returnedOrderView(APIView):
    def get(self, request, format=None):
        order_obj = Orders.objects.filter(returned=True)
        if order_obj:
            serializer = getOrdersSerializer(order_obj, many=True, context={'request': request})
            return Response({"data": serializer.data, "status": status.HTTP_200_OK, "success": "Orders Fetched Successfully"})
        else:
            return Response({"data": [], "status": status.HTTP_400_BAD_REQUEST, "message": "Orders do not found"})

class cancelorder(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, id, format=None):
        user = request.user
        # if user.is_authenticated:
        try:
            is_cancelled = Orders.objects.filter(id=id, user=request.user.id, cancelled=True)
            if not is_cancelled:
                order = Orders.objects.get(id=id, user=request.user.id, delivered=False)
                order.cancelled = True
                order.save()
                print(order)
                return Response({"status": status.HTTP_200_OK, "success": "Order Cancelled Successfully"})
            else:
                return Response({'message': 'Already Cancelled'}, status=status.HTTP_404_NOT_FOUND)
        except Orders.DoesNotExist:
            return Response({'error': 'Order Not Found'}, status=status.HTTP_404_NOT_FOUND)
        # else:
        #     return Response({"data": [], "error": status.HTTP_400_BAD_REQUEST, "message": "User not found"})

# class cancelorder(APIView):
#     authentication_classes = [authentication.TokenAuthentication]
#     permission_classes = [permissions.IsAuthenticated]

#     def post(self, request, id, format=None):
#         try:
#             order = Orders.objects.get(id=id, user=request.user)
            
#             if order.cancelled:
#                 return Response({'message': 'Order is already cancelled'}, status=status.HTTP_400_BAD_REQUEST)
            
#             if order.delivered:
#                 return Response({'message': 'Cannot cancel a delivered order'}, status=status.HTTP_400_BAD_REQUEST)
            
#             order.cancelled = True
#             order.save()
            
#             return Response({"status": status.HTTP_200_OK, "success": "Order Cancelled Successfully"})
        
#         except Orders.DoesNotExist:
#             return Response({'error': 'Order Not Found'}, status=status.HTTP_404_NOT_FOUND)