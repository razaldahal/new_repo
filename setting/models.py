from django.db import models
from main.models import BaseModel
# Create your models here.
class InstitutionDetail(BaseModel):
    key=models.CharField(max_length=150,unique=True)
    value=models.CharField(max_length=150)
    logo=models.ImageField(null=True,default='')