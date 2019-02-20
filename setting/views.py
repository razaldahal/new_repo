from django.shortcuts import render
from rest_framework.views import APIView
# Create your views here.
from .models import InstitutionDetail

from rest_framework.response import Response
from rest_framework import status,viewsets
class InstitutuionDetailsViewset(viewsets.ViewSet):
    queryset=InstitutionDetail.objects.all()
    def pre_save(self, obj):
        obj.logo = self.request.FILES.get('file')
    def create(self,request):
        
        print(request.data)
        setting=request.data
        if request.data=={}:
            return Response({"Error":"blank data"},status=status.HTTP_400_BAD_REQUEST)
        else:
            pass    

        for k,v in setting.items():

            try:
                a=InstitutionDetail.objects.get(key=k)
                a.value=v
                a.save()
            except:
                InstitutionDetail.objects.update_or_create(key=k,value=v)
                                  
        return Response('Created',status=status.HTTP_201_CREATED)



    def list(self,request):
        output={}
        lst=[]
        for obj in InstitutionDetail.objects.all():
            output['id']=obj.id
            output[obj.key]=obj.value
        lst.append(output)
        return Response(output)    

                 



