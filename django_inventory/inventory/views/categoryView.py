from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework import authentication, permissions
from inventory.models.categoryModel import *
from inventory.serializers.categorySerializer import *
from inventory.models.itemModel import *
from django.db import IntegrityError

class get_categories(APIView):
    def get(self, request, format=None):
        cat = Categories.objects.all()
        if cat:
            serializer = categorySerializer(cat, many=True)
            return Response({"data": serializer.data, "status": status.HTTP_200_OK, "success": "Categories Fetched Successfully"})
        else:
            return Response({"data": [], "status": status.HTTP_200_OK, "success": "Categories Fetched Successfully"})

class get_subcategories(APIView):
    def get(self, request, format=None):
        subcat = Subcategories.objects.all()
        if subcat:
            serializer = subcategorySerializer(subcat, many=True)
            return Response({"data": serializer.data, "status": status.HTTP_200_OK, "success": "Subcategories Fetched Successfully"})
        else:
            return Response({"data": [], "status": status.HTTP_200_OK, "success": "Subcategories Fetched Successfully"})

class get_subcat_by_catid(APIView):
    def get(self, request, id, format=None):
        subcat = Subcategories.objects.filter(category=id)
        if subcat:
            serializer = subcategorySerializer(subcat, many=True)
            return Response({"data": serializer.data, "status": status.HTTP_200_OK, "success": "Subcategories Fetched Successfully"})
        else:
            return Response({"data": [], "status": status.HTTP_200_OK, "success": "Subcategories Fetched Successfully"})

class get_subcat_by_cat(APIView):
    def get(self, request, id, format=None):
        cat = Categories.objects.filter(id=id)
        if cat:
            serializer = getsubcategorySerializer(cat, many=True)
            return Response({"data": serializer.data, "status": status.HTTP_200_OK, "success": "Subcategories Fetched Successfully"})
        else:
            return Response({"data": [], "status": status.HTTP_200_OK, "success": "Subcategories Fetched Successfully"})

class get_cat_subcat(APIView):
    def get(self, request, format=None):
        cat = Categories.objects.all()
        if cat:
            serializer = getsubcategorySerializer(cat, many=True)
            return Response({"data": serializer.data, "status": status.HTTP_200_OK, "success": "Subcategories Fetched Successfully"})
        else:
            return Response({"data": [], "status": status.HTTP_200_OK, "success": "Subcategories Fetched Successfully"})

class add_categories(APIView):
    def post(self, request, format=None):
        data = request.data
        print("add cat data" , data)
        data['name'] = data['name'].capitalize()
        subcategories = data.get('subcategory', [])
        try:
            if subcategories:
                add_cat = Categories.objects.create(name=data['name'])
                cat_id = add_cat.id
                for subcat in subcategories:
                    subcat = subcat.capitalize()
                    Subcategories.objects.create(name=subcat, category_id=cat_id)
                
                return Response({"data": [], "status": status.HTTP_201_CREATED, "message": "Category added successfully"})
            else:
                serializer = categorySerializer(data = request.data)
                if serializer.is_valid ():
                    serializer.save ()
                    data = serializer.data
                    return Response({"data": data, "status": status.HTTP_201_CREATED, "message": "Category addedd successfully"})
                return Response({"data": serializer.errors, "status": status.HTTP_400_BAD_REQUEST, "error": "Something went wrong"})
        except IntegrityError:
            return Response({'error': 'Category already exists.'}, status=status.HTTP_400_BAD_REQUEST)

class add_subcategories(APIView):
    def post(self, request, format=None):
        data = request.data
        print("add subcat" ,request.data)
        category = data.get('category')
        subcategories = data.get('subcategory', [])
        if subcategories and category:
            subcategories_data = []
            for subcategory in subcategories:
                capital = subcategory.capitalize()
                print(capital)
                already_exist = Subcategories.objects.filter(name = capital, category=category)
                if already_exist:
                    return Response({'error': 'Subcategory already exists.'}, status=status.HTTP_400_BAD_REQUEST)
                
                subcategory_data = {'name': capital, 'category': category}
                subcategories_data.append(subcategory_data)

                serializer = subcategorySerializer(data=subcategory_data)
                if serializer.is_valid ():
                    serializer.save ()
                    data = serializer.data
                else:
                    return Response({"data": [], "status": status.HTTP_400_BAD_REQUEST, "message": "Something went wrong"})
            return Response({"data": [], "status": status.HTTP_201_CREATED, "message": "Subcategory added successfully"})
        else:
            return Response({"data": [], "status": status.HTTP_400_BAD_REQUEST, "message": "All the fields are required"})
        # data['name'] = data['name'].capitalize()

        # already_exist = Subcategories.objects.filter(name = data['name'], category=data['category'])
        # if already_exist:
        #     return Response({'error': 'Subcategory already exists.'}, status=status.HTTP_400_BAD_REQUEST)
        # serializer = subcategorySerializer(data=request.data)
        # if serializer.is_valid ():
        #     serializer.save ()
        #     data = serializer.data
        #     return Response({"data": data, "status": status.HTTP_201_CREATED, "message": "Subcategory added successfully"})
       
        
    