from rest_framework import serializers

class InstitutionDetailSerializer(serializers.Serializer):
    logo=serializers.ImageField(required=False)
    


