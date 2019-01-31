from rest_framework import serializers
from admission.serializers import UserSerializer,PhoneSerializer,AddressSerializer
from student.models import Student
from .models import GUARDIAN_TYPE

class GuardianSerializer(serializers.Serializer):
	user = UserSerializer()
	guardian_type = serializers.ChoiceField(choices=GUARDIAN_TYPE)
	phone_detail=PhoneSerializer()
	address_detail=AddressSerializer()
	

class GuardianStudentSerializer(serializers.Serializer):
	guardian = GuardianSerializer()
	student = serializers.IntegerField()


