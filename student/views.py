from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from dashboard.views import get_current_year
from main.models import User
from .serializers import *

def generate_username(input_username):
    input_username = input_username.replace('_', '')
    input_username = input_username.lower()
    user = User.objects.filter(username__startswith=input_username.lower()).order_by('-date_created')
    if not user:
        return input_username + '_' + '1'
    else:
        print ('all users..',user)
        user = user.first()
        name, digit = user.username.split('_')
        digit = int(digit) + 1
        
        return '{}_{}'.format(input_username,digit)


class StudentAdmissionViewSet(ModelViewSet):

    queryset = Student.objects.all()
    serializer_class = StudentAdmissionSerializer
    http_method_names = ['post']


    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            data = serializer.data

            ud = data['user']

            if 'username' in ud:
                print ('this student is already registered . so just update...')
                return Response(data)


            username = generate_username(ud['first_name'])
            print(username)
            ud['type'] = 3

            user, c = User.objects.get_or_create(
                    username = username,
                    defaults = {**ud}
                )


            student = {'user':user.id, 'registration_no':data['registration_no']}
            student = StudentPostSerializer(data=student)
            if student.is_valid():
                raise serializers.ValidationError({'Detail':[student.errors]})

            student = student.save()

            if data.get('father', False):
                father,c = Guardian.objects.get_or_create(
                    student=student,
                    type='father',
                    defaults = { **data.get('father')}
                    )

            if data.get('mother', False):
                mother,c = Guardian.objects.get_or_create(
                    student=student,
                    type='mother',
                    defaults = { **data.get('mother')}
                    )


            if data.get('address', False):
                c = ContentType.objects.get_for_model(student)
                Address.objects.get_or_create(
                    content_type=c,
                    object_id=student.id,
                    defaults={ **data.get('address') }
                    )

            year = get_current_year()
            if year:
                year = year.name
            else:
                year = ''

            params = {
                'academic_year':year,
                'student':student,
                '_class':data['_class']
            }
            defaults = {}
            if 'section' in data:
                defaults['section'] = data['section']
            if 'admission_date' in data:
                defaults['admission_date'] = data['admission_date']

            StudentEnroll.objects.create(**params, defaults={**defaults})
            return Response(data)

        else:
            raise serializers.ValidationError({'Detail':[serializer.errors]})



class StudentViewSet(ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    http_method_names = ['get', 'post', 'put', 'delete']

    def get_serializer(self, *args, **kwargs):
        serializer_class = self.get_serializer_class()
        if self.request.method in ['POST', 'PUT']:
            serializer_class = StudentPostSerializer

        return serializer_class(*args, **kwargs)


    def create(self,request):
        serializer=self.get_serializer(data=request.data)
        if serializer.is_valid():

            data=serializer.data
            student, c = Student.objects.get_or_create(name=data.pop('name').title(), defaults=data)
            if not c:
                raise serializers.ValidationError({'Detail': ['{} student already exists'.format(course.name)]})

            data = StudentSerializer(student).data
            return Response(data)
        else:
            raise serializers.ValidationError({'Detail':[serializer.errors]})

def get_search_params(request):
    params = request.GET
    filter_params = {}
    whitelist_params = ['name']
    for k,v in params.items():
    	if k == 'name':
    		filter_params['user__first_name__iexact'.format(k)] = v
    return filter_params


class StudentSearchViewSet(APIView):

    def search(self):
        output = []
        filter_params = get_search_params(self.request)
        if filter_params:
            students = Student.objects.filter(**filter_params)
            
            students = StudentSerializer(students, many=True)
            output = students.data
        return output

    @swagger_auto_schema(manual_parameters=[
        
        openapi.Parameter('name', openapi.IN_QUERY, type=openapi.TYPE_STRING),
        ])
    def get(self, request, format=None):
        """
        Student search
        """
        #output = self.search()
        output = [
        	{'id':1 , 'registration_no':'034490', 'user':{'first_name':'ashish', 'last_name':'belwase'}},
            {'id':2 , 'registration_no':'034491', 'user':{'first_name':'ram', 'last_name':'khanal'}}
        ]
        return Response(output)

