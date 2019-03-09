from rest_framework import serializers
from main.serializers import UserPostSerializer,AddressSerializer
from student.serializers import GuardianSerializer
from student.models import *
from main.models import *
from transport.models import *

class StudentSerializer(serializers.ModelSerializer):
    user = UserPostSerializer()
    class Meta:
        model = Student
        fields = ('user','registration_no')
    # registration_no = serializers.IntegerField()


class StudentReportSerializer(serializers.ModelSerializer):
    student = StudentSerializer()
    class_name = serializers.CharField(source='_class.name')
    # course_name = serializers.CharField(source='_class.course.name')
    section = serializers.CharField(source='section.name', required=False)
    admission_date = serializers.DateTimeField(format='%Y%B%d')
    class Meta:
        model = StudentEnroll
        fields = ('student','class_name','section','admission_date')

class VehicleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vehicle
        fields = ('start_location','stop_location')

class StudentVehicleReportSerializer(serializers.ModelSerializer):
    student = StudentSerializer()
    vehicle  = VehicleSerializer(required=False)
    class Meta:
        model = VehicleAllocation
        fields = ('__all__')


