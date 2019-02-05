from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from main.models import User, Address
from .models import *


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



class UserPostSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    type = serializers.IntegerField(required=False, default=3)  #  3 = student
    username = serializers.CharField(required=False)
    email = serializers.CharField(required=False, allow_null=True)
    first_name = serializers.CharField(required=True, allow_null=True)
    middle_name = serializers.CharField(required=False, allow_null=True)
    last_name = serializers.CharField(required=True)
    gender = serializers.IntegerField(required=False, allow_null=True)
    blood_group = serializers.IntegerField(required=False, allow_null=True)
    nationality = serializers.IntegerField(required=False, allow_null=True)
    religion = serializers.IntegerField(required=False, allow_null=True)
    citizenship_no = serializers.CharField(required=False, allow_null=True)
    date_of_birth = serializers.DateField(required=False, allow_null=True)
    current_address = serializers.CharField(required=False, allow_null=True)
    phone = serializers.CharField(required=False, allow_null=True)
    profile_pic = serializers.CharField(required=False, allow_null=True)
    class Meta:
        model = User
        fields = (
            'id',
            'type', 'username',
            'first_name', 'middle_name', 'last_name', 'email',
            'gender', 'blood_group',
            'nationality', 'religion', 'citizenship_no', 'date_of_birth', 
            'current_address', 'phone', 'profile_pic',
            )

        # validators = [
  #           UniqueTogetherValidator(
  #               queryset=User.objects.all(),
  #               fields=('username',)
  #           )
  #       ]


class AddressSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    class Meta:
        model = Address
        fields = ('id', 'province', 'city', 'district', 'address', )


class GuardianSerializer(serializers.ModelSerializer):
    #student = serializers.IntegerField(source='student.id')
    id = serializers.IntegerField(required=False)
    type = serializers.CharField(required=False)
    mobile = serializers.CharField(required=False, allow_null=True)
    job = serializers.CharField(required=False, allow_null=True)
    citizenship_no = serializers.CharField(required=False, allow_null=True)

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

    course_name = serializers.CharField(required=False)
    class_name = serializers.CharField(required=False)