from rest_framework import serializers
from admission.serializers import UserSerializer
from student.models import Student


class GuardianSerializer(serializers.Serializer):
	user = UserSerializer()
	guardian_type = serializers.IntegerField()

class GuardianStudentSerializer(serializers.Serializer):
	guardian = GuardianSerializer()
	student = serializers.IntegerField()


