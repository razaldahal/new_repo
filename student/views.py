from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework import status

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


def get_student_detail(obj, lis=True):
    f = obj.guardian.filter(type='father')
    if f:
        obj.father = f.first()
    m = obj.guardian.filter(type='mother')
    if m:
        obj.mother = m.first()

    c = ContentType.objects.get_for_model(obj)
    a = Address.objects.filter(content_type=c, object_id=obj.id)
    if a:
        obj.address = a.first()

    params = {'student':obj}
    if lis:
        params['academic_year'] = get_current_year()
    se = StudentEnroll.objects.filter(**params)
    # print('hsdjsdsdhf',se)
    if se:
        se = se.first()
        obj.admission_date = se.admission_date
        obj.course = se._class.course_id
        obj.course_name = se._class.course.name
        obj._class = se._class_id
        obj.class_name = se._class.name
        obj.section = se.section_id
        obj.roll_no = se.roll_no
    return obj

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
                student,boo = Student.objects.get_or_create(user_id=ud['id'],registration_no = data['registration_no'])
                if not boo:
                    raise serializers.ValidationError({
                        'Detail':['User_id & registration_no Should be Unique']
                        })
                year = get_current_year()
      
                params = {
                    'academic_year':year,
                    'student':student
                    }
                defaults = {
                    '_class_id':data['_class']
                    }
                if 'section' in data:
                    defaults['section_id'] = data['section']
                if 'admission_date' in data:
                    defaults['admission_date'] = data['admission_date']

                StudentEnroll.objects.get_or_create(**params, defaults={**defaults})
                return Response(data)

            username = generate_username(ud['first_name'])
            # print(username)
            ud['type'] = 3
            
            if ud['email'] is None:
                ud['email'] = username + '@btech.com'
                # print(ud)
                # print({}.format(ud['email']))
            user, c = User.objects.get_or_create(
                    username = username,
                    defaults = {**ud}
                )


            student = {'user_id':user.id, 'registration_no':data['registration_no']}
            student = StudentPostSerializer(data=student)
            if not student.is_valid():
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
            # print(year)

            params = {
                'academic_year':year,
                'student':student,
                'roll_no':data['roll_no']
                
            }
            defaults = {
                '_class_id':data['_class']
            }
            if 'section' in data:
                defaults['section_id'] = data['section']
            if 'admission_date' in data:
                defaults['admission_date'] = data['admission_date']

            StudentEnroll.objects.get_or_create(**params, defaults={**defaults})
            return Response(data)

        else:
            raise serializers.ValidationError({'Detail':[serializer.errors]})



class StudentViewSet(ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    http_method_names = ['get', 'put']

    def get_serializer(self, *args, **kwargs):
        serializer_class = self.get_serializer_class()
        if self.request.method in ['POST', 'PUT']:
            serializer_class = StudentAdmissionSerializer

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

    def list(self, request, *args, **kwargs):
        print(get_current_year())
        students = []
        objects = self.get_queryset()
        # objects = StudentEnroll.objects.filter(academic_year=get_current_year())
        section_id = request.GET.get('section_id', False)
        if section_id:
            objects = []
            _objects = StudentEnroll.objects.filter(section_id=section_id, academic_year=get_current_year())
            for obj in _objects:
                objects.append(obj.student)

        for obj in objects:
            students.append(get_student_detail(obj))
        
        students = StudentGetSerializer(students, many=True).data
        return Response(students)

    def retrieve(self, request, *args, **kwargs):
        obj = self.get_object()
        obj = get_student_detail(obj)
        student = StudentGetSerializer(obj).data
        return Response(student)

    def update(self, request, pk):
        instance = self.get_object()
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            data = serializer.data
            
            # UserPostSerializer().update(instance.user, data['user'])
            s = UserPostSerializer(instance.user, data['user'])
            if s.is_valid():
                s.save()
                
            address = Address.objects.get(id=data['address']['id'])
            AddressSerializer().update(address, data['address'])
            father = Guardian.objects.get(id=data['father']['id'])
            GuardianSerializer().update(father, data['father'])
            mother = Guardian.objects.get(id=data['mother']['id'])
            GuardianSerializer().update(mother, data['mother'])

            return Response(data)

        else:
            raise serializers.ValidationError({'Detail':[serializer.errors]})




class StudentImageViewSet(APIView):

    def post(self, request, *args, **kwargs):
        print(request.POST)
        print (request.FILES)
        if 'file' in request.FILES and 'student_id' in request.POST:
            file = request.FILES['file']
            student = Student.objects.get(id=int(request.POST['student_id']))
            student.user.profile_pic = file
            student.user.save()

        return Response({})

def get_search_params(request):
    params = request.GET
    filter_params = {}
    whitelist_params = ['q']
    for k,v in params.items():
    	if k == 'q' and len(v) > 2:
    		filter_params['user__first_name__icontains'.format(k)] = v
    return filter_params


class StudentSearchViewSet(APIView):

    def search(self):
        output = []
        filter_params = get_search_params(self.request)
        if filter_params:
            print(filter_params)
            students = []
            objects = Student.objects.filter(**filter_params)
            # print('{}objects'.format(objects))
            for obj in objects:
                obj = get_student_detail(obj, False)

                students.append(obj)

            students = StudentGetSerializer(students, many=True)
            output = students.data
        return output

    @swagger_auto_schema(manual_parameters=[
        
        openapi.Parameter('q', openapi.IN_QUERY, type=openapi.TYPE_STRING),
        ])
    def get(self, request, format=None):
        """
        Student search
        """
        output = self.search()
        # output = [
        # 	{'id':1 , 'registration_no':'034490', 'user':{'first_name':'ashish', 'last_name':'belwase'}},
        #     {'id':2 , 'registration_no':'034491', 'user':{'first_name':'ram', 'last_name':'khanal'}}
        # ]
        return Response(output)

