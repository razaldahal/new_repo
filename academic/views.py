from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from .serializers import *


class AcademicYearViewSet(ModelViewSet):
    queryset = AcademicYear.objects.all()
    serializer_class = AcademicYearSerializer
    http_method_names = ['post', 'get']

    def list(self, request):
        data = self.get_serializer(self.queryset.filter(is_active=True).first()).data
        return Response(data)

    def create(self,request):
        serializer=self.get_serializer(data=request.data)
        if serializer.is_valid():
            data=serializer.data

            ## first make all false
            for obj in self.queryset:
                obj.is_active = False
                obj.save()


            ay, c = AcademicYear.objects.get_or_create(name=data.pop('name'), defaults=data)
            ay.is_active = True
            ay.save()

            data = AcademicYearSerializer(ay).data
            return Response(data)
        else:
            raise serializers.ValidationError({'Detail':[serializer.errors]})


class CourseViewSet(ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    http_method_names = ['get', 'post', 'put', 'delete']

    def get_serializer(self, *args, **kwargs):
        serializer_class = self.get_serializer_class()
        if self.request.method == 'POST':
            serializer_class = CoursePostSerializer

        return serializer_class(*args, **kwargs)


    def create(self,request):
        serializer=self.get_serializer(data=request.data)
        if serializer.is_valid():
            data=serializer.data
            course, c = Course.objects.get_or_create(name=data.pop('name').title(), defaults=data)
            if not c:
                raise serializers.ValidationError({'Detail': ['{} course already exists'.format(course.name)]})

            data = CourseSerializer(course).data
            return Response(data)
        else:
            raise serializers.ValidationError({'Detail':[serializer.errors]})

class ClassViewSet(ModelViewSet):
    queryset = Class.objects.all()
    serializer_class = ClassSerializer
    http_method_names = []



class CourseClassViewSet(ModelViewSet):
    queryset = Class.objects.filter().order_by('-date_created')
    serializer_class = ClassSerializer
    
    http_method_names = ['get', 'post', 'delete']



    def get_serializer(self, *args, **kwargs):
        serializer_class = self.get_serializer_class()
        if self.request.method == 'POST':
            serializer_class = ClassPostSerializer
        return serializer_class(*args, **kwargs)

    def list(self, request, course_pk, pk=None):
        queryset = self.queryset.filter(course_id=course_pk).all()
        output = self.get_serializer(queryset, many=True).data
        return Response(output)


    def create(self,request, course_pk):
        serializer=self.get_serializer(data=request.data)
        if serializer.is_valid():
            data=serializer.data
            course = False
            try:
                course = Course.objects.get(id=course_pk)
            except:
                raise serializers.ValidationError({'Detail':['No such course']})
            else:

                _class, c = Class.objects.get_or_create(course=course, name=data['name'], defaults={'description':data['description']})
                if not c:
                    raise serializers.ValidationError({'Detail': ['{} class already exists'.format(_class.name)]})

                data = ClassSerializer(_class).data
                return Response(data)
        else:
            raise serializers.ValidationError({'Detail':[serializer.errors]})

class ClassSectionViewSet(ModelViewSet):
    queryset = Section.objects.filter().order_by('-date_created')
    serializer_class = SectionSerializer
    
    http_method_names = ['get', 'post', 'delete']



    def get_serializer(self, *args, **kwargs):
        serializer_class = self.get_serializer_class()
        if self.request.method == 'POST':
            serializer_class = SectionPostSerializer
        return serializer_class(*args, **kwargs)

    def list(self, request, class_pk, pk=None):
        queryset = self.queryset.filter(_class_id=class_pk).all()
        output = self.get_serializer(queryset, many=True).data
        return Response(output)


    def create(self,request, class_pk):
        serializer=self.get_serializer(data=request.data)
        if serializer.is_valid():
            data=serializer.data
            _class = False
            try:
                _class = Class.objects.get(id=class_pk)
            except:
                raise serializers.ValidationError({'Detail':['No such class']})
            else:

                section, c = Section.objects.get_or_create(_class=_class, name=data['name'])
                if not c:
                    raise serializers.ValidationError({'Detail': ['{} section already exists'.format(section.name)]})

                data = SectionSerializer(section).data
                return Response(data)
        else:
            raise serializers.ValidationError({'Detail':[serializer.errors]})




