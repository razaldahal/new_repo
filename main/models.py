from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import fields


class BaseModel(models.Model):
	date_created = models.DateField(auto_now_add=True)
	date_updated = models.DateField(auto_now=True)
	date_deleted = models.DateField(null=True,blank=True)

	class Meta:
		abstract = True

USER_TYPE=(
	('ADMINISTRATOR',1),
	('TEACHER' , 2),
	('STUDENT' , 3),
	('GUEST' , 4),
	('ACCOUNTANT' ,5),
	('LIBRARIAN' ,6),
	)

GENDER =(
	('MALE',1),
	('FEMALE',2),
	('OTHERS',3)
	)

class User(BaseModel, AbstractUser):
	type = models.IntegerField(choices=USER_TYPE,null=True)
	gender = models.IntegerField(choices=GENDER,null=True)


TYPE =(
	('PHONE',1),
	('LANDLINE',2),
	('CDMA',3),
	)


class Phone(BaseModel):
	content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True)
	object_id = models.PositiveIntegerField(null=True)
	content_object = fields.GenericForeignKey('content_type', 'object_id')

	type = models.IntegerField(choices=TYPE)
	number = models.IntegerField()

class Address(BaseModel):
	content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True)
	object_id = models.PositiveIntegerField(null=True)
	content_object = fields.GenericForeignKey('content_type', 'object_id')

	province = models.CharField(max_length=120)
	district = models.CharField(max_length=120)
	city = models.CharField(max_length=120)
	address = models.CharField(max_length=120) ## eg. ramjanaki tole, bharatpur

RELIGION=(
	('HINDU',1),
	('MUSLIM',2),
	)

class UserDetail(BaseModel):
	user = models.ForeignKey(User,on_delete=models.CASCADE)
	blood_group = models.CharField(max_length=5)
	nationality = models.CharField(max_length=120)
	mother_tongue = models.CharField(max_length=120)
	religion = models.IntegerField(choices=RELIGION)
	citizenship_no = models.CharField(max_length=10)


