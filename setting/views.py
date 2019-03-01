from rest_framework import status,viewsets
from rest_framework.views import APIView
from rest_framework.response import Response

from .serializers import *

class InstitutuionDetailsViewset(viewsets.ModelViewSet):
    queryset=InstitutionDetail.objects.all()
    serializer_class=InstitutionDetailSerializer

    def create(self,request):
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
        qst=InstitutionDetail.objects.all().exclude(key='csrfmiddlewaretoken')
        for obj in qst:
            output['id']=obj.id
            output[obj.key]=obj.value
            
        lst.append(output)
        
        return Response(output)    

class CollegeLogo(APIView):
    # http_method_names = ['GET','POST']
    # if request.method == "GET":
    #     print("hello ET")

    def get(self,request):
        obj = Media.objects.all().first()
        data = MediaGetSerializer(obj).data
        return Response({'logo':data['logo']})

    def post(self, request, *args, **kwargs):
        print(request.POST)
        print (request.FILES)
        if 'file' in request.FILES:
            file = request.FILES['file']
            Media.objects.update_or_create(file_name='College_Name',
                                            defaults={
                                                'logo':file
                                                }
                                                )
        return Response({})
