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

        output = getInstituteDetail()

        return Response(output)    

class CollegeLogo(APIView):
    # http_method_names = ['GET','POST']
    # if request.method == "GET":
    #     print("hello ET")

    def get(self,request):
        output = getInstituteLogo()
        return Response(output)

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
