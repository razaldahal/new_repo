from django.shortcuts import render
from rest_framework.views import APIView
# Create your views here.
from rest_framework.parsers import MultiPartParser,JSONParser,FileUploadParser,FormParser
from .models import InstitutionDetail
from .serializers import InstitutionDetailSerializer
from rest_framework.response import Response
from rest_framework import status,viewsets
class InstitutuionDetailsViewset(viewsets.ModelViewSet):
    queryset=InstitutionDetail.objects.all()
    serializer_class=InstitutionDetailSerializer
    parser_classes=(MultiPartParser,FormParser,JSONParser,FileUploadParser)

    def create(self,request):
        
        print(request.POST)
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
                InstitutionDetail.objects.update_or_create(key=k,value=v,logo = self.request.FILES.get('logo'))
                                  
        return Response('Created',status=status.HTTP_201_CREATED)



    def list(self,request):
        output={}
        lst=[]
        qst=InstitutionDetail.objects.all().exclude(key='csrfmiddlewaretoken')
        for obj in qst:
            if not obj.logo:
                output['id']=obj.id
                output[obj.key]=obj.value
            else:
                 output['logo']=obj.logo.url  
            
        lst.append(output)
        
        return Response(output)    

                 



