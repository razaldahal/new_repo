from rest_framework import serializers
from main.models import RELIGION,TYPE,GENDER,USER_TYPE,User
from main.helpers.tuple import get_choice_string
from student.models import Student
choices=(
		('Father','FATHER'),
		('Mother','MOTHER'),
		('Both','BOTH')
		)

class UserBaseSerializer(serializers.Serializer):
	first_name = serializers.CharField(max_length=120,required=True)
	last_name = serializers.CharField(max_length=120,required=True)
	email = serializers.EmailField(required=True)
	


class UserSerializer(UserBaseSerializer):
	gender = serializers.ChoiceField(choices=GENDER)
	type = serializers.IntegerField(default=3)
	
	

class UserGetSerializer(UserBaseSerializer):
	gender = serializers.SerializerMethodField()
	type = serializers.IntegerField(default=3)
	def get_gender(self, obj):
		return get_choice_string(GENDER,obj.gender)

class UserDetailSerializer(serializers.Serializer):
	blood_group = serializers.CharField(max_length=120,required=True)
	nationality = serializers.CharField(max_length=120)
	mother_tongue = serializers.CharField(max_length=120)
	religion = serializers.IntegerField()
	citizenship_no = serializers.CharField()


class PhoneSerializer(serializers.Serializer):
	type = serializers.IntegerField(default=1)
	number = serializers.IntegerField(required=True)


class AddressSerializer(serializers.Serializer):
	province = serializers.CharField(max_length=120,required=True)
	district = serializers.CharField(max_length=120,required=True)
	city = serializers.CharField(max_length=120,required=True)
	address = serializers.CharField(required=True)
class oldparentserializer(serializers.Serializer):
	type=serializers.ChoiceField(choices=choices)
	name=serializers.CharField(max_length=40)
	mobile=serializers.CharField(max_length=20)
	job=serializers.CharField(max_length=30)
	citizenship=serializers.CharField(max_length=10)	

class FatherSerializer(serializers.Serializer):
	name=serializers.CharField(max_length=40)
	mobile=serializers.CharField(max_length=20)
	job=serializers.CharField(max_length=30)
	citizenship_no=serializers.CharField(max_length=10)

class MotherSerializer(serializers.Serializer):
	name=serializers.CharField(max_length=40)
	mobile=serializers.CharField(max_length=20)
	job=serializers.CharField(max_length=30)
	citizenship_no=serializers.CharField(max_length=10)


class StudentAdmissionBaseSerializer(serializers.Serializer):
	user = UserSerializer()
	user_detail = UserDetailSerializer()
	phone_detail = PhoneSerializer()
	address_detail = AddressSerializer()
	registration_no = serializers.IntegerField()
	batch = serializers.IntegerField()
	description = serializers.CharField(default='')
	
	#image = serializers.ImageField()
	father=FatherSerializer()
	mother=MotherSerializer()



class StudentAdmissionGetSerializer(StudentAdmissionBaseSerializer):
	id = serializers.IntegerField()
	course = serializers.CharField()
	

class StudentAdmissionSerializer(StudentAdmissionBaseSerializer):
	course = serializers.IntegerField()



class StudentUpdateSerializer(StudentAdmissionBaseSerializer):
	pass