from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from main.models import User, Address
from .models import *


class StudentPostSerializer(serializers.ModelSerializer):

    class Meta:
        model = Student
        fields = ('user', 'registration_no',)
    
class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ('id', 'registration_no', )



class UserPostSerializer(serializers.ModelSerializer):
    type = serializers.IntegerField(required=False, default=3)  #  3 = student
    username = serializers.CharField(required=False)
    email = serializers.CharField(required=False)
    first_name = serializers.CharField(required=True)
    middle_name = serializers.CharField(required=False)
    last_name = serializers.CharField(required=True)
    gender = serializers.IntegerField(required=False)
    blood_group = serializers.IntegerField(required=False)
    nationality = serializers.IntegerField(required=False)
    religion = serializers.IntegerField(required=False)
    citizenship_no = serializers.CharField(required=False)
    date_of_birth = serializers.DateField(required=False)
    current_address = serializers.CharField(required=False)
    class Meta:
        model = User
        fields = (
            'type', 'username',
            'first_name', 'middle_name', 'last_name', 'email',
            'gender', 'blood_group',
            'nationality', 'religion', 'citizenship_no', 'date_of_birth', 
            'current_address'
            )

        # validators = [
  #           UniqueTogetherValidator(
  #               queryset=User.objects.all(),
  #               fields=('username',)
  #           )
  #       ]


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ('province', 'city', 'district', 'address', )


class GuardianSerializer(serializers.ModelSerializer):
    student = serializers.IntegerField(source='student.id')
    type = serializers.CharField(required=False, default='father')
    mobile = serializers.CharField(required=False)
    job = serializers.CharField(required=False)
    citizenship_no = serializers.CharField(required=False)

    class Meta:
        model = Guardian
        fields = ('student', 'type', 'name','mobile',  'job', 'mobile', 'citizenship_no', )

        validators = [
            UniqueTogetherValidator(
                queryset=Guardian.objects.all(),
                fields=('student', 'type')
            )
        ]


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
