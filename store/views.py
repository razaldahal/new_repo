from django.shortcuts import render
from rest_framework import viewsets
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework import status

from .models import *
from .serializers import *

class VendorViewSet(viewsets.ModelViewSet):
    queryset = VendorModel.objects.all()
    serializer_class = VendorSerializer

class ProductCategoryViewSet(viewsets.ModelViewSet):
    queryset = ProductCategory.objects.all()
    serializer_class = ProductCategorySerializer

class ProductsViewSet(viewsets.ViewSet):
    queryset = ProductsModel.objects.all()

    def create(self,request):
        serializer = ProductsSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.data
            obj,boo = ProductsModel.objects.get_or_create(vendor_id=data['vendor'],
                                                        category_id = data['category'],
                                                        item_name = data['item_name'],
                                                        defaults={
                                                            'quantity':data['quantity'],
                                                            'rate':data['rate'],
                                                            'discount':data['discount']
                                                        })
            if not boo:
                raise serializers.ValidationError({
                    'Detail':['Items With This Category & Vendor Already Exist']
                })
            return Response(data,status=status.HTTP_201_CREATED)
        else:
            raise serializers.ValidationError({
                'Detail':[serializer.errors]
            })

    def list(self,request):
        objects = self.queryset
        data = request.GET
        select_type = int(data['select_type'])
        if select_type == 0:
            output = []
            for obj in objects:
                temp = {
                    'id' :obj.id,
                    'vendor':obj.vendor.name,
                    'category':obj.category.name,
                    'item_name':obj.item_name,
                    'quantity':obj.quantity,
                    'rate':obj.rate,
                    'discount':obj.discount
                }
                output.append(temp)
            return Response(output,status=status.HTTP_200_OK)
        else:
            category_id = data['category_id']
            category_id = int(category_id)
            
            output = []
            objects =  ProductsModel.objects.all().filter(category_id=category_id)
            for obj in objects:
                temp = {
                    'id' :obj.id,
                    'vendor':obj.vendor.name,
                    'category':obj.category.name,
                    'item_name':obj.item_name,
                    'quantity':obj.quantity,
                    'rate':obj.rate,
                    'discount':obj.discount
                }
                output.append(temp)
            return Response(output,status=status.HTTP_200_OK)