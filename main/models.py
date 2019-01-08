from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import fields
from rest_framework.decorators import api_view
from .helpers.tuple import get_choice_string


class BaseModel(models.Model):
    date_created = models.DateField(auto_now_add=True)
    date_updated = models.DateField(auto_now=True)
    date_deleted = models.DateField(null=True,blank=True)


    class Meta:
        abstract = True

USER_TYPE=(
    (1,'ADMINISTRATOR'),
    (2,'TEACHER'),
    (3,'STUDENT'),
    (4,'GUEST'),
    (5,'ACCOUNTANT'),
    (6,'LIBRARIAN'),
    (7,'BUSSTAFF')
    )

GENDER =(
    (1,'MALE'),
    (2,'FEMALE'),
    (3,'OTHERS'),
    )

    
TYPE =(
    (1,'PHONE'),
    (2,'LANDLINE'),
    (3,'CDMA'),
    )

RELIGION=(
    (1, 'HINDU'),
    (2, 'MUSLIM'),
    )

NATIONALITY=(
    (1, 'Nepali'),
    (2, 'Hindi'),
    )

class User(BaseModel, AbstractUser):
    type = models.IntegerField(choices=USER_TYPE,null=True)
    middle_name = models.CharField(null=True, blank=True, max_length=255)
    token = models.CharField(null=True, blank=True, max_length=255)
    gender = models.IntegerField(choices=GENDER ,null=True)
    blood_group = models.IntegerField(null=True, blank=True)
    nationality = models.IntegerField(choices=NATIONALITY,null=True, blank=True)
    religion = models.IntegerField(choices=RELIGION,null=True, blank=True)
    citizenship_no = models.CharField(max_length=10,null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    current_address = models.TextField()

    class Meta:
        db_table = 'main_user'
        verbose_name_plural = "User"

    def __str__(self):
        return self.username
    

class Address(BaseModel):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True)
    object_id = models.PositiveIntegerField(null=True)
    content_object = fields.GenericForeignKey('content_type', 'object_id')
    
    province = models.CharField(max_length=120)
    district = models.CharField(max_length=120)
    city = models.CharField(max_length=120)
    address = models.CharField(max_length=120) ## eg. ramjanaki tole, bharatpur

    class Meta:
        db_table = 'main_address'
        verbose_name_plural = "Address"

    def __str__(self):
        return self.address + ',' + self.city


