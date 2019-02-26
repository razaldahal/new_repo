from rest_framework.response import Response
from rest_framework import viewsets,status
from rest_framework.viewsets import ModelViewSet

from django.contrib.contenttypes.models import ContentType


from main.models import Address
from .serializers import *


def get_faculty_detail(obj):
    c = ContentType.objects.get_for_model(obj)
    a = Address.objects.filter(content_type=c, object_id=obj.id)
    if a:
        obj.address = a.first()

    return obj

class FacultyViewSet(ModelViewSet):

    queryset = Faculty.objects.all()
    serializer_class = FacultySerializer
    http_method_names = ['post', 'get', 'put', 'delete']

    def get_serializer_class(self, *args, **kwargs):
        # if self.request.method == 'GET':
        #     return FacultyGetSerializer
        return FacultySerializer


    def list(self, request, *args, **kwargs):
        faculties = []
        objects = self.queryset
        for obj in objects:
            faculties.append(get_faculty_detail(obj))

        faculties = FacultySerializer(faculties, many=True).data
        return Response(faculties)

    def retrieve(self, request, *args, **kwargs):
        obj = self.get_object()
        obj = get_faculty_detail(obj)
        faculty = FacultySerializer(obj).data
        return Response(faculty)

    def update(self, request, pk):
        instance = self.get_object()
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            data = serializer.data

            instance.qualification = data['qualification']
            instance.save()

            ## check email
            try:
                user = User.objects.filter(email=data['user']['email']).exclude(id=instance.id)
                if user:
                    raise serializers.ValidationError({'Detail':['Email is already registered. Please use another.']})

            except:
                pass
            
            s = UserPostSerializer(instance.user, data['user'])
            if s.is_valid():
                s.save()
            address = Address.objects.get(id=data['address']['id'])
            AddressSerializer().update(address, data['address'])
            return Response(data)



        else:
            raise serializers.ValidationError({'Detail':[serializer.errors]})




    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            data = serializer.data

            ud = data['user']

            # try:
            #     user = User.objects.get(email=ud['email'])
            #     serializers.ValidationError({'Detail':['Email is already registered. Please use another.']})
            # except Exception as ex:
            #     print (ex)
            #     pass

            user, c = User.objects.get_or_create(
                    username = ud['email'],
                    defaults = {**ud}
                )

            if not c:
                raise serializers.ValidationError({'Detail':['Email is already registered. Please use another.']})


            faculty = {'user_id':user.id, 'qualification':data['qualification']}
            faculty = Faculty.objects.create(**faculty)


            if data.get('address', False):
                address = data['address']
                c = ContentType.objects.get_for_model(faculty)
                Address.objects.get_or_create(
                    content_type=c,
                    object_id=faculty.id,
                    defaults=address
                    )

            return Response(data)

        else:
            raise serializers.ValidationError({'Detail':[serializer.errors]})

