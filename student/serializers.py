from rest_framework import serializers

class StudentAssignmentSerializer(serializers.Serializer):
	assignment_id = serializers.IntegerField()
	section_student_id = serializers.IntegerField()
	status = serializers.IntegerField()
	
class StudentAssignmentDetail(serializers.Serializer):
	name = serializers.CharField(max_length=120)
	status = serializers.IntegerField()

class AssStdSectionSerializer(serializers.Serializer):
	first_name = serializers.CharField(max_length=120)
	last_name = serializers.CharField(max_length=120)


class TestStudentSerializer(serializers.Serializer):
	section_student_id = serializers.IntegerField()
	test_id = serializers.IntegerField()
	mark_obtained = serializers.IntegerField()

class TestDetailGet(serializers.Serializer):
	date = serializers.DateField()
	type = serializers.IntegerField()
	full_marks = serializers.IntegerField()
	pass_marks = serializers.IntegerField()