from django.shortcuts import render
from rest_framework.views import APIView
# Create your views here.
from .models import InstitutionDetail
from .serializers import InstitutionSerializer
from rest_framework.response import Response
from rest_framework import status,viewsets
class InstitutuionDetailsViewset(viewsets.ModelViewSet):
    queryset=InstitutionDetail.objects.all()
    serializer_class=InstitutionSerializer
    def create(self,request):
        serializer=self.get_serializer(data=request.data)
        if serializer.is_valid():
            data=serializer.data
            klist=['name','address','email','phone']
            if data['key'] in klist:
                try:
                    InstitutionDetail.objects.update_or_create(key=data['key'],value=data['value'])
                except Exception:
                    return Response({'Error':'Key must be unique'},status=status.HTTP_409_CONFLICT)   
            else:
                return Response('Input valid key',status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'Detail':[serializer.errors]},status=status.HTTP_400_BAD_REQUEST)        
        return Response('Created',status=status.HTTP_201_CREATED)



    def list(self,request):
        output={}
        lst=[]
        for obj in InstitutionDetail.objects.all():
            output['id']=obj.id
            output[obj.key]=obj.value
        lst.append(output)
        return Response(output)    

                 



