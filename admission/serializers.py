from rest_framework import serializers
from main.models import RELIGION,TYPE,GENDER,USER_TYPE
from main.helpers.tuple import reverse_tuple_lookup
from student.models import Student

class UserBaseSerializer(serializers.Serializer):
	first_name = serializers.CharField(max_length=120,required=True)
	last_name = serializers.CharField(max_length=120,required=True)
	email = serializers.EmailField(required=True)
	
	
class UserSerializer(UserBaseSerializer):
	gender = serializers.IntegerField()
	type = serializers.IntegerField(default=3)


class UserGetSerializer(UserBaseSerializer):
	gender = serializers.IntegerField()
	type = serializers.IntegerField(default=3)

	# def get_gender(self, obj):
	# 	return {'id':obj.gender, 'value':reverse_tuple_lookup(obj.gender, GENDER)}
	
class UserDetailSerializer(serializers.Serializer):
	blood_group = serializers.CharField(max_length=120,required=True)
	nationality = serializers.CharField(max_length=120)
	mother_tongue = serializers.CharField(max_length=120)
	religion = serializers.IntegerField()
	citizenship_no = serializers.CharField(required=False)


class PhoneSerializer(serializers.Serializer):
	type = serializers.IntegerField(default=1)
	number = serializers.IntegerField(required=True)


class AddressSerializer(serializers.Serializer):
	province = serializers.CharField(max_length=120,required=True)
	district = serializers.CharField(max_length=120,required=True)
	city = serializers.CharField(max_length=120,required=True)
	address = serializers.CharField(required=True)

class ParentSerializer(serializers.Serializer):
	name = serializers.CharField(max_length=120,required=True)
	mobile = serializers.CharField(max_length=120,required=True)
	job = serializers.CharField(max_length=120,required=False)
	citizen_no = serializers.CharField(max_length=120,required=False)


class StudentAdmissionBaseSerializer(serializers.Serializer):
	user = UserSerializer()
	user_detail = UserDetailSerializer()
	phone_detail = PhoneSerializer()
	address_detail = AddressSerializer()
	registration_no = serializers.IntegerField()
	batch = serializers.IntegerField()
	description = serializers.CharField(default='')
	father = ParentSerializer()
	mother = ParentSerializer()
	#image = serializers.ImageField()


class StudentAdmissionGetSerializer(StudentAdmissionBaseSerializer):
	id = serializers.IntegerField()
	course = serializers.CharField()
	

class StudentAdmissionSerializer(StudentAdmissionBaseSerializer):
	course = serializers.IntegerField()