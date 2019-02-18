from .models import InstitutionDetail

from rest_framework import serializers
class InstitutionSerializer(serializers.Serializer):
    key=serializers.CharField()
    value=serializers.CharField()
    logo=serializers.ImageField(default=None,required=False)