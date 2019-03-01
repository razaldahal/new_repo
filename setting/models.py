from django.db import models
from main.models import BaseModel

class InstitutionDetail(BaseModel):
    key=models.CharField(max_length=150,unique=True)
    value=models.CharField(max_length=150)
    
class Media(BaseModel):
    file_name = models.CharField(max_length=120)
    logo = models.ImageField(upload_to = 'Colleges_Logo/', null=True, blank=True)
    