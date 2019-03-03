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


def getInstituteDetail():
    output={}
    qst=InstitutionDetail.objects.all().exclude(key='csrfmiddlewaretoken')
    for obj in qst:
        output['id']=obj.id
        output[obj.key]=obj.value
    return output

def getInstituteLogo():
    obj = Media.objects.filter(file_name='College_Name').first()
    output = {}
    if obj:
        data = MediaGetSerializer(obj).data
        output = {'logo':data['logo']}
    return output

