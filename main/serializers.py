from rest_framework import serializers
from .models import User, Address

class UserPostSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    type = serializers.IntegerField(required=False, default=3)  #  3 = student
    username = serializers.CharField(required=False)
    email = serializers.CharField(required=False, allow_null=True,allow_blank=True)
    first_name = serializers.CharField(required=True, allow_null=True)
    middle_name = serializers.CharField(required=False, allow_null=True)
    last_name = serializers.CharField(required=True)
    gender = serializers.IntegerField(required=False, allow_null=True)
    blood_group = serializers.IntegerField(required=False, allow_null=True)
    nationality = serializers.IntegerField(required=False, allow_null=True)
    religion = serializers.IntegerField(required=False, allow_null=True)
    citizenship_no = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    date_of_birth = serializers.DateField(required=False, allow_null=True)
    current_address = serializers.CharField(required=False, allow_null=True)
    phone = serializers.CharField(required=False, allow_null=True)
    profile_pic = serializers.CharField(required=False, allow_null=True, allow_blank=True)
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

