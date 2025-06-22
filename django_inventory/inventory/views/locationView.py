from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, reverse
from rest_framework.views import APIView
from rest_framework.renderers import JSONRenderer
from django.http import JsonResponse
from rest_framework import status
from rest_framework.response import Response
from rest_framework import authentication, permissions
from inventory.models import *
from inventory.serializers.locationSerializer import *
from inventory.serializers.itemsSerializer import *
from django.db.models import Count

class LocationView(APIView):
    def get(self, request, format=None):
        locations = Locations.objects.all()
        if locations:
            items = Items.objects.all()
            serializer = locationSerializer(locations, many=True)
            return Response({"data": serializer.data, "status": status.HTTP_200_OK, "success": "Locations Fetched Successfully"})
        else:
            return Response({"data": [], "status": status.HTTP_200_OK, "success": "Items Fetched Successfully"})
            
class ItemsByLocationId(APIView):
    def get(self, request, id, format=None):
        location_obj = Locations.objects.get(id = id)
        items_count = len(Items.objects.filter(location=id))
        items = Items.objects.filter(location=id).values("name", "category__name", "subcategory__name", "price", "weight", "quantity").annotate(count=Count("name"))
        if items:
            return Response({"data": items,"name" : location_obj.name, "total_stock" : items_count, "status": status.HTTP_200_OK, "success": "Items Fetched Successfully"})
        else:
            return Response({"data": [], "status": status.HTTP_400_BAD_REQUEST, "message": "Items do not found"})

class ItemsLocationView(APIView):
    def get(self, request, format=None):
        items = Items.objects.all().values("name", "category__name", "subcategory__name", "price", "weight", "quantity")
        items_count = len(Items.objects.all())
        if items:
            return Response({"data": items, "total_stock" : items_count , "status": status.HTTP_200_OK, "success": "Items Fetched Successfully"})
        else:
            return Response({"data": [], "status": status.HTTP_400_BAD_REQUEST, "message": "Items do not found"})

class LocationByItems(APIView):
    def post(self, request, format=None):
        sku_number = request.data['sku_number']
        item = Items.objects.filter(SKU_number=sku_number)
        location = item['location']
        print(location)
