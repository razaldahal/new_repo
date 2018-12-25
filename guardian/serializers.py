from rest_framework import serializers
from admission.serializers import *
from student.models import Student


class GuardianSerializer(serializers.Serializer):
	user = UserSerializer()
	guardian_type = serializers.IntegerField()
	phone_detail=PhoneSerializer()
	address_deatail=AddressSerializer()
	

class GuardianStudentSerializer(serializers.Serializer):
	guardian = GuardianSerializer()
	student = serializers.IntegerField()


