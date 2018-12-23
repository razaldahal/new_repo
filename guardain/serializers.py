from rest_framework import serializers
from admission.serializers import UserSerializer

class GuardianSerializer(serializers.Serializer):
	user = UserSerializer()
	guardian_type = serializers.IntegerField()