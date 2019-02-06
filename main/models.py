from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import fields
from django import forms
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
	(7,'BUSSTAFF'),
	(8,'GUARDIAN'),
	)

GENDER =(
	(1,'MALE'),
	(2,'FEMALE'),
	(3,'OTHERS'),
	)

class User(BaseModel, AbstractUser):
	type = models.IntegerField(choices=USER_TYPE,null=True,blank=True)
	gender = models.IntegerField(choices=GENDER ,null=True ,blank=True)


	
	
	
TYPE =(
	(1,'PHONE'),
	(2,'LANDLINE'),
	(3,'CDMA'),
	)


class Phone(BaseModel):
	content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True)
	object_id = models.PositiveIntegerField(null=True)
	content_object = fields.GenericForeignKey('content_type', 'object_id')

	type = models.IntegerField(choices=TYPE)
	number = models.CharField(max_length=15)
class Parent(BaseModel):
	content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True)
	object_id = models.PositiveIntegerField(null=True)
	content_object = fields.GenericForeignKey('content_type', 'object_id')
	type=models.CharField(max_length=10)
	name=models.CharField(max_length=40)
	mobile=models.CharField(max_length=20)
	job=models.CharField(max_length=30)
	citizenship_no=models.CharField(max_length=10)


class Address(BaseModel):
	content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True)
	object_id = models.PositiveIntegerField(null=True)
	content_object = fields.GenericForeignKey('content_type', 'object_id')


	
	province = models.CharField(max_length=120)
	district = models.CharField(max_length=120)
	city = models.CharField(max_length=120)
	address = models.CharField(max_length=120) ## eg. ramjanaki tole, bharatpur

RELIGION=(
	(1,'HINDU'),
	(2,'MUSLIM'),
	)

class UserDetail(BaseModel):
	user = models.ForeignKey(User,on_delete=models.CASCADE)
	blood_group = models.CharField(max_length=5)
	nationality = models.CharField(max_length=120)
	mother_tongue = models.CharField(max_length=120)
	religion = models.CharField(choices=RELIGION,max_length=7)
	citizenship_no = models.CharField(max_length=10)


