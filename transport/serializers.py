from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator


#from admission.serializers import UserBaseSerializer,UserSerializer,USER_TYPE,PhoneSerializer,AddressSerializer
from student.models import Student
from student.views import get_student_detail
from .models import *

class StaffSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    class Meta:
        model = Staff
        fields = '__all__'
            

class VehicleSerializer(serializers.ModelSerializer):
    staff=serializers.PrimaryKeyRelatedField(queryset=Staff.objects.all())
    class Meta:
        model = Vehicle
        fields = '__all__'

class VehicleGetSerializer(VehicleSerializer):
    staff = StaffSerializer()


class VehicleAllocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = VehicleAllocation
        fields = '__all__'
        validators = [
            UniqueTogetherValidator(
                queryset=VehicleAllocation.objects.all(),
                fields=('student', 'vehicle'),
                message=('This vehicle is already allocated to student.')
            )
        ]

class VehicleAllocationGetSerializer(VehicleAllocationSerializer):
    student = serializers.SerializerMethodField()
    vehicle = VehicleSerializer()

    def get_student(self, obj):
        return {'id':obj.student_id, 'name':obj.student.user.first_name + ' ' + obj.student.user.last_name}
