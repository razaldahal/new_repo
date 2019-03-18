from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from .models import *
from student.models import *


class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = ('name','description','code','id')

class ClassSubjectSerializer(serializers.ModelSerializer):
    class_name = serializers.CharField(source='_class.name')
    subject = serializers.CharField(source='subject.name')
    id = serializers.IntegerField(source="subject.id")
    class Meta:
        model = AssignSubject
        fields = ('id','class_name','subject')


class ExamTermSerializer(serializers.ModelSerializer):
    _class_id = serializers.IntegerField()
    class Meta:
        model = ExamTerm
        fields = ('name','start_date','end_date','_class_id')
        validators = [
            UniqueTogetherValidator(
                queryset=ExamTerm.objects.all(),
                fields=('name','_class_id'),
                message="Exam Name & Class Name Should Be Unique"
            )
        ]



class ExamScheduleSerializer(serializers.Serializer):
    exam = serializers.IntegerField()
    subject = serializers.IntegerField()
    date = serializers.DateField()
    start_time = serializers.TimeField()
    end_time = serializers.TimeField()


class MarksTypeGetSerializer(serializers.Serializer):
    full_marks = serializers.IntegerField(default=0)
    full_marks_th = serializers.IntegerField(default=0)
    full_marks_pr = serializers.IntegerField(default=0)
    pass_marks = serializers.IntegerField(default=0)
    pass_marks_th = serializers.IntegerField(default=0)
    pass_marks_pr = serializers.IntegerField(default=0)

class MarksEntryGetSerializer(serializers.ModelSerializer):
    student_name = serializers.SerializerMethodField()
    theory = serializers.IntegerField(default=0)
    practical = serializers.IntegerField(default=0)
    # total = serializers.SerializerMethodField()
    id = serializers.IntegerField(source='student.id')
    full_marks = serializers.IntegerField(default=0,source='marks_entry.full_marks')
    full_marks_th = serializers.IntegerField(default=0,source='marks_entry.full_marks_th')
    full_marks_pr = serializers.IntegerField(default=0,source='marks_entry.full_marks_pr')
    pass_marks = serializers.IntegerField(default=0,source='marks_entry.pass_marks')
    pass_marks_th = serializers.IntegerField(default=0,source='marks_entry.pass_marks_th')
    pass_marks_pr = serializers.IntegerField(default=0,source='marks_entry.pass_marks_pr')
      
    class Meta:
        model = MarksEntryDetail
        fields = ('id','student_name','theory','practical','full_marks',
                        'full_marks_th','full_marks_pr','pass_marks',
                            'pass_marks_th','pass_marks_pr',)
        # depth = 1

    def get_student_name(self,obj):
        return '{} {}'.format(obj.student.user.first_name,obj.student.user.last_name)
    # def get_total(self,obj):
    #     return obj.theory + obj.practical

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
    discipline = serializers.IntegerField(default=0)



class ResultPrepareViewSet(serializers.ModelSerializer):
    total = serializers.SerializerMethodField()
    student_name = serializers.SerializerMethodField()
    student_id = serializers.IntegerField(source='student.id')
    class Meta:
        model = MarksEntryDetail
        fields = ('theory','practical','discipline','total','student_name','student_id')

    def get_total(self,obj):
        return obj.theory + obj.practical + obj.discipline

    def get_student_name(self,obj):
        return '{} {}'.format(obj.student.user.first_name,obj.student.user.last_name)



class PrepareResultClassWiseSerializer(serializers.ModelSerializer):
    student = serializers.SerializerMethodField()
    subject = serializers.SerializerMethodField()
    class Meta:
        model = MarksEntryDetail
        fields = ('student','subject','theory','practical')
        # depth = 2
    def get_student(self,obj):
        return obj.student.user.first_name
    def get_subject(self,obj):
        return obj.marks_entry.subject.name


class GradingSerializer(serializers.ModelSerializer):
    marks_ratio = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = GradingSystem
        fields = ('id','marks_from','marks_to','grade_division','explanation',
                    'grade_point','marks_ratio')
        validators = [
            UniqueTogetherValidator(
                queryset=GradingSystem.objects.all(),
                fields=('grade_division','explanation','grade_point'),
                # message="Exam Name & Class Name Should Be Unique"
            )
        ]
    def get_marks_ratio(self,obj):
        return '{} To {}'.format(obj.marks_from,obj.marks_to)
