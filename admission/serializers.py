from rest_framework import serializers
from main.models import RELIGION,TYPE,GENDER,USER_TYPE,User
from main.helpers.tuple import get_choice_string
from student.models import Student
from guardian.models import GUARDIAN_TYPE
from Section.serializers import SectionSerializer
from transport.models import Route
from course.models import Batch,Course
from accountant.models import payment_type_c,PaymentType,Payments,Accountant,discount_type_c
from Class.models import Class

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
	type = serializers.ChoiceField(choices=USER_TYPE,required=False)
	def get_type(self, obj):
		return get_choice_string(USER_TYPE,obj.type)
	
	

class UserGetSerializer(UserBaseSerializer):
	gender = serializers.SerializerMethodField()
	type = serializers.IntegerField(default=3)
	def get_gender(self, obj):
		return get_choice_string(GENDER,obj.gender)

class UserDetailSerializer(serializers.Serializer):
	blood_group = serializers.CharField(max_length=120,required=True)
	nationality = serializers.CharField(max_length=120)
	mother_tongue = serializers.CharField(max_length=120)
	religion = serializers.ChoiceField(choices=RELIGION)
	citizenship_no = serializers.CharField()


class PhoneSerializer(serializers.Serializer):
	type = serializers.IntegerField(default=1)
	number = serializers.CharField(required=True)


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
class GuardianSerializer(serializers.Serializer):
	guser = UserSerializer()
	guardian_type = serializers.ChoiceField(choices=GUARDIAN_TYPE)
	phone_detail=PhoneSerializer()
	address_detail=AddressSerializer()
class TransportAllocationSerializer(serializers.Serializer):
    route=serializers.PrimaryKeyRelatedField(queryset=Route.objects.all())
class PaymentTypeSerializer(serializers.Serializer):
    _class=serializers.PrimaryKeyRelatedField(queryset=Class.objects.all())
    name=serializers.ChoiceField(choices=payment_type_c)
    rate=serializers.IntegerField()
    def get_name(self,obj):
        return get_choice_string(payment_type_c,obj.name)	
class PaymentsSerializer(serializers.Serializer):
    payment_type=PaymentTypeSerializer()
    paid_method=serializers.IntegerField()
    paid_by=UserSerializer()
    paid_for=serializers.PrimaryKeyRelatedField(queryset=Student.objects.all())
    paid_to=serializers.PrimaryKeyRelatedField(queryset=Accountant.objects.all())
    paid_amount=serializers.IntegerField()
    short_description=serializers.CharField()
    cheque_no=serializers.CharField(required=False)
    discount_type=serializers.ChoiceField(choices=discount_type_c)
    total_discount_amount=serializers.IntegerField(required=False)
    discount_description=serializers.CharField()
    fine_amount=serializers.IntegerField()
    fine_description=serializers.CharField()
		
class StudentAdmissionBaseSerializer(serializers.Serializer):
	user = UserSerializer()
	user_detail = UserDetailSerializer()
	phone_detail = PhoneSerializer()
	address_detail = AddressSerializer()
	registration_no = serializers.IntegerField()
	batch = serializers.IntegerField()
	description = serializers.CharField(default='')
	section=SectionSerializer()
	guardian=GuardianSerializer()
	#image = serializers.ImageField()
	student_payment_ac=PaymentsSerializer()
	transport = TransportAllocationSerializer()
	father=FatherSerializer()
	mother=MotherSerializer()



class StudentAdmissionGetSerializer(StudentAdmissionBaseSerializer):
	id = serializers.IntegerField()
	course = serializers.CharField()
	

class StudentAdmissionSerializer(StudentAdmissionBaseSerializer):
	course = serializers.IntegerField()



class StudentUpdateSerializer(serializers.Serializer):
	user = UserSerializer()
	user_detail = UserDetailSerializer()
	phone_detail = PhoneSerializer()
	address_detail = AddressSerializer()
	registration_no = serializers.IntegerField()
	batch = serializers.PrimaryKeyRelatedField(queryset=Batch.objects.all())
	description = serializers.CharField(default='')
	
	#image = serializers.ImageField()
	father=FatherSerializer()
	mother=MotherSerializer()
	course = serializers.IntegerField()
