from rest_framework import serializers


class SubjectSerializer(serializers.Serializer):
	name = serializers.CharField(max_length=120)
	description = serializers.CharField(max_length=120)
	code = serializers.CharField(max_length=15)


class ExamTermSerializer(serializers.Serializer):
    name = serializers.CharField()
    start_date = serializers.DateField()
    end_date = serializers.DateField()
    course = serializers.IntegerField()
    _class = serializers.IntegerField()

    def validate(self,data):
        if data['start_date'] > data['end_date']:
            raise serializers.ValidationError("Start Date Should be smaller") 
        return data

class ExamUpdateSerializer(serializers.Serializer):
    name = serializers.CharField(required=False)
    start_date = serializers.DateField(required=False)
    end_date = serializers.DateField(required=False)
    course = serializers.IntegerField(required=False)
    _class = serializers.IntegerField(required=False)

    def partial_update(self,instance,data):
        instance.name = data.get('name',instance.name)
        instance.course_id = data.get('course',instance.course)
        instance._class_id = data.get('_class',instance._class)
        instance.start_date = data.get('start_date',instance.start_date)
        instance.end_date = data.get('end_date',instance.end_date)
        instance.save()
        return instance

class ExamScheduleSerializer(serializers.Serializer):
    exam = serializers.IntegerField()
    subject = serializers.IntegerField()
    date = serializers.DateField()
    start_time = serializers.TimeField()
    end_time = serializers.TimeField()

class MarksTypeSerializer(serializers.Serializer):
    full_marks = serializers.IntegerField()
    full_marks_th = serializers.IntegerField()
    full_marks_pr = serializers.IntegerField()
    pass_marks = serializers.IntegerField()
    pass_marks_th = serializers.IntegerField()
    pass_marks_pr = serializers.IntegerField()

class StudentMarksSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    theory = serializers.IntegerField()
    practical = serializers.IntegerField()
    discipline = serializers.IntegerField(default=0)

class MarksEntrySerializer(serializers.Serializer):
    section = serializers.IntegerField()
    exam = serializers.IntegerField()
    subject = serializers.IntegerField()
    marks_type = MarksTypeSerializer()
    student_data = serializers.ListField()

