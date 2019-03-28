from datetime import datetime

from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from main.models import User, Address
from main.serializers import UserPostSerializer, AddressSerializer
from .models import *


def getBirthdays():
    output = []
    today = datetime.now().date()
    print(today.month, today.day)
    sts = StudentEnroll.objects.filter(
        student__user__date_of_birth__month=today.month,
        student__user__date_of_birth__day=today.day,

        )
    for s in sts:
        output.append({
                'id':s.student.id,
                'first_name': s.student.user.first_name,
                'last_name': s.student.user.last_name,
                'course': s._class.course.name,
            })
    return output

class StudentPostSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField()
    registration_no = serializers.CharField()
    class Meta:
        model = Student
        fields = ('user_id', 'registration_no',)
    
class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ('id', 'registration_no', )



class GuardianSerializer(serializers.ModelSerializer):
    #student = serializers.IntegerField(source='student.id')
    id = serializers.IntegerField(required=False)
    type = serializers.CharField(required=False)
    mobile = serializers.CharField(required=False, allow_null=True)
    job = serializers.CharField(required=False, allow_null=True)
    citizenship_no = serializers.CharField(required=False,allow_null=True, allow_blank=True)

    class Meta:
        model = Guardian
        fields = ('id', 'type', 'name','mobile',  'job', 'mobile', 'citizenship_no', )

        # validators = [
        #     UniqueTogetherValidator(
        #         queryset=Guardian.objects.all(),
        #         fields=('type')
        #     )
        # ]


class StudentAdmissionSerializer(serializers.Serializer):
    registration_no = serializers.CharField()
    course = serializers.IntegerField()
    _class = serializers.IntegerField()
    roll_no = serializers.IntegerField()
    section = serializers.IntegerField(required=False)
    admission_date = serializers.DateTimeField(required=False)
    user = UserPostSerializer()
    address = AddressSerializer()
    father = GuardianSerializer()
    mother = GuardianSerializer()



class StudentGetSerializer(StudentAdmissionSerializer):
    id = serializers.IntegerField()
    address = AddressSerializer(required=False)
    father = GuardianSerializer(required=False)
    mother = GuardianSerializer(required=False)
    roll_no = serializers.IntegerField()

    course_name = serializers.CharField(required=False)
    class_name = serializers.CharField(required=False)