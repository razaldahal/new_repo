from rest_framework import serializers

class SectionSerializer(serializers.Serializer):
	_class_id =  serializers.IntegerField()
	name = serializers.CharField()

class SectionStudentSerializer(serializers.Serializer):
	student_id = serializers.IntegerField()
	section_id = serializers.IntegerField()
	roll_no = serializers.IntegerField()

class TeacherSectionSerializer(serializers.Serializer):
	subject_id = serializers.IntegerField()
	section_id = serializers.IntegerField()
	teacher_id = serializers.IntegerField()

class SectionRoutineSerializer(serializers.Serializer):
	teacher_section_id = serializers.IntegerField()
	day_of_week = serializers.DateField()
	start_time = serializers.TimeField()
	end_time = serializers.TimeField()