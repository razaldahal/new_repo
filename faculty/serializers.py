from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from main.serializers import UserPostSerializer, User, AddressSerializer
from academic.models import Faculty

class FacultySerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    user = UserPostSerializer()
    address = AddressSerializer()
    class Meta:
        model = Faculty
        fields = ('id', 'user', 'qualification', 'address', )
            

# class FacultyPostSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Faculty
#         fields = '__all__'
#         validators = [
#             UniqueTogetherValidator(
#                 queryset=VehicleAllocation.objects.all(),
#                 fields=('student', 'vehicle'),
#                 message=('This vehicle is already allocated to student.')
#             )
#         ]

# class FacultyGetSerializer(VehicleAllocationSerializer):
#     student = serializers.SerializerMethodField()
#     vehicle = VehicleSerializer()

#     def get_student(self, obj):
#         return {'id':obj.student_id, 'name':obj.student.user.first_name + ' ' + obj.student.user.last_name}
