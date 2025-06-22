from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, reverse
from rest_framework.views import APIView
from rest_framework.renderers import JSONRenderer
from django.http import JsonResponse
from rest_framework import status
from rest_framework.response import Response
from rest_framework import authentication, permissions
from inventory.serializers.itemsSerializer import *
from inventory.models import *
import base64
from django.core.files.base import ContentFile

class itemView(APIView):

    def get(self, request, format=None):
        items = Items.objects.filter().order_by('-added_on')
        if items:
            serializer = getitemsSerializer(items, many=True, context={'request': request})
            return Response({"data": serializer.data, "status": status.HTTP_200_OK, "success": "Items Fetched Successfully"})
        else:
            return Response({"data": [], "status": status.HTTP_400_BAD_REQUEST, "message": "Items do not found"})
      
    def post(self, request, format=None):
        count = request.data.get('count')
        data = request.data
        image_data = request.data.get('image_data')
        if image_data:
            decoded_image = base64.b64decode(image_data)
            file_name = 'image.jpg'
            image_file = ContentFile(decoded_image, name=file_name)

            request.data['image'] = image_file
        serializer = postitemsSerializer(data = request.data)
        if serializer.is_valid ():
            serializer.save (is_available = True)
            data = serializer.data
            data['created_by'] = request.user.id
            return Response({"data": data, "code": status.HTTP_201_CREATED, "message": "Item added successfully"})
        else:
            return Response({"data": serializer.errors, "status": status.HTTP_400_BAD_REQUEST, "error": "Something went wrong"})
    
        # try:
        #     for _ in range(int(count)):
        #         data = request.data
        #         serializer = postitemsSerializer(data = request.data)
        #         if serializer.is_valid ():
        #             serializer.save ()
        #             data = serializer.data
        #             print("data", data)
        #             data['created_by'] = request.user.id
        #         else:
        #             return Response({"data": serializer.errors, "status": status.HTTP_400_BAD_REQUEST, "error": "Something went wrong"})
        #     return Response({"data": data, "code": status.HTTP_201_CREATED, "message": "Item added successfully"})
        # except Exception as e:
        #     print(e)
        #     return Response({'error': 'Something went wrong.'}, status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request, id, format=None):
        try:
            data = request.data
            print(data)
            item = Items.objects.get(id = id)
            serializer = updateItemSerializer(item, data=data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({"data": serializer.data, "code": status.HTTP_200_OK, "message": "Item Updated Successfully"})
            else:
                return Response({"error": serializer.errors, "code": status.HTTP_400_BAD_REQUEST, "message": "Something went wrong"})
        except Items.DoesNotExist:
            return Response({"data": [], "code": status.HTTP_400_BAD_REQUEST, "message": "Item do not found"})
        
    def delete(self, request, id, format=None):
        try:
            item_obj = Items.objects.get(id = id)
        except Items.DoesNotExist:
            return Response({"code": status.HTTP_400_BAD_REQUEST, "message": "Item not found"})
        item_obj.delete()
        return Response({"code": status.HTTP_200_OK, "message": "Item deleted successfully"})

class get_item_by_id(APIView):
    def get(self, request, id , format=None):
        item_id = Items.objects.get(id = id)
        if item_id:
            serializer = getitemsSerializer(item_id, context={'request': request})
            return Response({"data": serializer.data, "status": status.HTTP_200_OK, "success": "Items Fetched Successfully"})
        else:
            return Response({"data": [], "status": status.HTTP_400_BAD_REQUEST, "message": "Items do not found"})
      
class get_items_by_catid(APIView):
    def get(self, request, id, format=None):
        items_obj = Items.objects.filter(category=id).order_by('-added_on')
        if items_obj:
            context = {"catid": id, "request" : request}
            serializer = getitemsSerializer(items_obj, many=True, context=context)
            return Response({"data": serializer.data, "status": status.HTTP_200_OK, "success": "Items Fetched Successfully"})
        else:
            return Response({"data": [], "status": status.HTTP_200_OK, "success": "Items Fetched Successfully"})

class get_items_by_subid(APIView):
    def get(self, request, cid, sid, format=None):
        items_obj = Items.objects.filter(category=cid, subcategory=sid).order_by('-added_on')
        if items_obj:
            serializer = getitemsSerializer(items_obj, many=True, context={'request':request})
            return Response({"data": serializer.data, "status": status.HTTP_200_OK, "success": "Items Fetched Successfully"})
        else:
            return Response({"data": [], "status": status.HTTP_200_OK, "success": "Items Fetched Successfully"})

class addImage(APIView):
    def post(self, request, format=None):
        price = request.data['price']
        cat_id = request.data['category']
        sku = request.data['SKU_number']
        cat = Categories.objects.get(id = cat_id)
        image_data = request.data['image_data']
        decoded_image = base64.b64decode(image_data)
        file_name = 'image.jpg'
        image_file = ContentFile(decoded_image, name=file_name)
        item = Items.objects.create(price=price, image=image_file, category=cat, SKU_number=sku)
        # Return the saved image object
        return item.image
