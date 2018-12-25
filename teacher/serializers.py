from rest_framework import serializers

from admission.serializers import UserSerializer,PhoneSerializer,AddressSerializer

from .models import Subject

class TeacherAddSerializer(serializers.Serializer):
	user_detail = UserSerializer()
	phone_detail = PhoneSerializer()
	address_detail = AddressSerializer()
	qualification = serializers.CharField(max_length=120)

class TeacherUpdateSerializer(serializers.Serializer):
	phone_detail = PhoneSerializer()
	address_detail = AddressSerializer()
	qualification = serializers.CharField(max_length=120)

class SubjectSerializer(serializers.Serializer):
	name = serializers.CharField(max_length=120)
	description = serializers.CharField(max_length=120)
	code = serializers.CharField(max_length=15)
class AssignmentSerializer(serializers.Serializer):
	teacher_section_id = serializers.IntegerField()
	due_date = serializers.DateField()
	priority = serializers.CharField(max_length=120)
	status = serializers.IntegerField()
	name = serializers.CharField(max_length=120)
	description = serializers.CharField(max_length=120)

class TeacherDetailAssignment(serializers.Serializer):
	first_name = serializers.CharField(max_length=120)
	last_name = serializers.CharField(max_length=120)

class SubjectDetailAssignment(serializers.Serializer):
	name = serializers.CharField(max_length=120)

class AssignmentDetail(serializers.Serializer):
	due_date = serializers.DateField()
	priority = serializers.CharField(max_length=120)
	status = serializers.IntegerField()
	name = serializers.CharField(max_length=120)
	description = serializers.CharField(max_length=120)


class ResourcesSerializer(serializers.Serializer):
	teacher_id = serializers.IntegerField()
	name = serializers.CharField(max_length=120)
	description = serializers.CharField(max_length=120)

class ResourceDetailSerializer(serializers.Serializer):
	name = serializers.CharField(max_length=120)
	description = serializers.CharField(max_length=120)

class TestSerializer(serializers.Serializer):
	teacher_id = serializers.IntegerField()
	date = serializers.DateField()
	type = serializers.IntegerField()
	full_marks = serializers.IntegerField()
	pass_marks = serializers.IntegerField()