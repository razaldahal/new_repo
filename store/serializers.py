from rest_framework import serializers
from .models import *

class VendorSerializer(serializers.ModelSerializer):
    class Meta:
        model  = VendorModel
        fields = ('id','name','description')

class ProductCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model  = ProductCategory
        fields = ('id','name','description')

class ProductsSerializer(serializers.ModelSerializer):
    vendor = serializers.IntegerField()
    category = serializers.IntegerField()
    class Meta:
        model = ProductsModel
        fields = ('id','vendor','category','item_name',
                    'quantity','rate','discount')