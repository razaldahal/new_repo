from django.db import models
from main.models import BaseModel

class VendorModel(BaseModel):
    name = models.CharField(max_length=120)
    description = models.CharField(max_length=200)

class ProductCategory(BaseModel):
    name = models.CharField(max_length=120)
    description = models.CharField(max_length=200)

class ProductsModel(BaseModel):
    vendor = models.ForeignKey(VendorModel,on_delete=models.CASCADE)
    category = models.ForeignKey(ProductCategory,on_delete=models.CASCADE)
    item_name = models.CharField(max_length=120)
    quantity = models.IntegerField()
    rate = models.IntegerField()
    discount = models.IntegerField()