
from rest_framework import viewsets,status
from rest_framework.views import APIView
from rest_framework.response import Response

from academic.models import AcademicYear, Course, Class, Faculty
from student.serializers import Student, getBirthdays
from accounting.serializers import getTodayCollection, getTotalDue
from setting.serializers import getInstituteDetail, getInstituteLogo


def get_current_year():
    academic_year = AcademicYear.objects.filter(is_active=True).first()
    if academic_year:
        return academic_year
    return False

class StatsViewSet(APIView):
    
    def get(self,request):    
        employee = Faculty.objects.count()
        student = Student.objects.count()
        course = Course.objects.count()
        _class = Class.objects.count()

        output ={
            'count':{
                'employee':employee,
                'student':student,
                'course':course,
                'class':_class
                },
            'academic':{},
            'accounting': {'today_collection': getTodayCollection(), 'total_dues':getTotalDue()},
            'institute': getInstituteDetail(),
            'birthdays': getBirthdays()
        }

        output['institute'].update(getInstituteLogo())

        academic_year = get_current_year()
        if academic_year:
            output['academic']['year'] = academic_year.name
        return Response(output)

