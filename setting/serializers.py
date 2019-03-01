from rest_framework import serializers
from .models import *

class InstitutionDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = InstitutionDetail
        fields = ('__all__')
class MediaGetSerializer(serializers.ModelSerializer):
    logo = serializers.CharField(source='logo.name')
    class Meta:
        model = Media
        fields = ['logo']