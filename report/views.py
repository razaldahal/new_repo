from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response

from main.models import User
from student.models import *
from library.models import *
from transport.models import *

from .serializers import *
from student.serializers import *
from main.serializers import *
from library.serializers import *

from django_filters.rest_framework import DjangoFilterBackend

class StudentFilterViewSet(ModelViewSet):
    queryset = StudentEnroll.objects.all()
    serializer_class = StudentReportSerializer
    report = { }

    def get_student_report_transport(self,obj,sn):
        self.report = { } 
        student_id = obj.student.id
        print(student_id)
        co = StudentEnroll.objects.get(student__id = student_id)
        self.report['course'] = co._class.course.name
        self.report['sn'] = sn
       
        std_obj = obj.student
       
        g_obj = Guardian.objects.filter(student__id=student_id,type='father')
        father_detail = GuardianSerializer(g_obj,many=True).data
        
        g_obj = Guardian.objects.filter(student__id=student_id,type='mother')
        mother_detail = GuardianSerializer(g_obj,many=True).data
        

        c = ContentType.objects.get_for_model(std_obj)
        a = Address.objects.filter(content_type=c, object_id=student_id)
        address_detail = AddressSerializer(a,many=True).data

        student_detail =  StudentVehicleReportSerializer(obj,).data
        student_detail['class_name'] = co._class.name
        student_detail['section'] = co.section.name
        student_detail['admission_date'] = co.admission_date
        self.report['father_detail'] = father_detail
        self.report['mother_detail'] = mother_detail
        self.report['student_detail'] = student_detail
        self.report['address_detail'] = address_detail
      
        return self.report



    
    def get_student_report(self,obj,sn):
        self.report = { } 
        self.report['sn'] = sn
        self.report['course'] = obj._class.course.name
        std_obj = obj.student
        student_id = obj.student.id
        g_obj = Guardian.objects.filter(student__id=student_id,type='father')
        father_detail = GuardianSerializer(g_obj,many=True).data
        
        g_obj = Guardian.objects.filter(student__id=student_id,type='mother')
        mother_detail = GuardianSerializer(g_obj,many=True).data
        

        c = ContentType.objects.get_for_model(std_obj)
        a = Address.objects.filter(content_type=c, object_id=student_id)
        address_detail = AddressSerializer(a,many=True).data

        student_detail =  StudentReportSerializer(obj,).data
        self.report['father_detail'] = father_detail
        self.report['student_detail'] = student_detail
        self.report['address_detail'] = address_detail
        self.report['mother_detail'] = mother_detail
        return self.report


    def list(self,request):
        self.report = {}
        data = request.GET
        print(data)
        output = []
        sn = 0

        for k,v in data.items():
            print(k)
            if k == 'gender':
                if data['reportby'] == 'allclass':
                    print('Gender',data['gender'])
                    objects = StudentEnroll.objects.filter(student__user__gender=data['gender'])
                    for obj in objects:
                        sn += 1
                        detail = self.get_student_report(obj,sn)
                        output.append(detail)
                    return Response(output)

                elif data['reportby'] == 'sectionwise':
                    objects = StudentEnroll.objects.filter(student__user__gender=data['gender'],_class__id=data['class'],section__id=data['section'])
                    for obj in objects:
                        sn += 1
                        detail = self.get_student_report(obj,sn)
                        output.append(detail)
                    return Response(output)
                else:
                    objects = StudentEnroll.objects.filter(student__user__gender=data['gender'],_class__id=data['class'])
                    for obj in objects:
                        sn += 1
                        detail = self.get_student_report(obj,sn)
                        output.append(detail)
                    return Response(output)
            elif k == 'blood_group':
                if data['reportby'] == 'allclass':
                    objects = StudentEnroll.objects.filter(student__user__blood_group=data['blood_group'])
                    for obj in objects:
                        sn += 1
                        detail = self.get_student_report(obj,sn)
                        output.append(detail)
                    return Response(output)

                elif data['reportby'] == 'sectionwise':
                    objects = StudentEnroll.objects.filter(student__user__blood_group=data['blood_group'],_class__id=data['class'],section__id=data['section'])
                    for obj in objects:
                        sn += 1
                        detail = self.get_student_report(obj,sn)
                        output.append(detail)
                    return Response(output)
                else:
                    objects = StudentEnroll.objects.filter(student__user__blood_group=data['blood_group'],_class__id=data['class'])
                    for obj in objects:
                        sn += 1
                        detail = self.get_student_report_transport(obj,sn)
                        output.append(detail)
                    return Response(output)
            elif k == 'religion':
                if data['reportby'] == 'allclass':
                    objects = StudentEnroll.objects.filter(student__user__religion=data['religion'])
                    for obj in objects:
                        sn += 1
                        detail = self.get_student_report(obj,sn)
                        output.append(detail)
                    return Response(output)

                elif data['reportby'] == 'sectionwise':
                    objects = StudentEnroll.objects.filter(student__user__religion=data['religion'],_class__id=data['class'],section__id=data['section'])
                    for obj in objects:
                        sn += 1
                        detail = self.get_student_report(obj,sn)
                        output.append(detail)
                    return Response(output)
                else:
                    objects = StudentEnroll.objects.filter(student__user__religion=data['religion'],_class__id=data['class'])
                    for obj in objects:
                        sn += 1
                        detail = self.get_student_report(obj,sn)
                        output.append(detail)
                    return Response(output)
            elif k == 'transport':
                if data['reportby'] == 'allclass':
                    objects = VehicleAllocation.objects.all()
                    for obj in objects:
                        sn += 1
                        detail = self.get_student_report_transport(obj,sn)
                        output.append(detail)

                    return Response(output)

                elif data['reportby'] == 'sectionwise':
                    objects = VehicleAllocation.objects.all()
                    for obj in objects:
                        sn += 1
                        detail = self.get_student_report_transport(obj,sn)
                        output.append(detail)
                    return Response(output)
                else:
                    objects = VehicleAllocation.objects.all()
                    for obj in objects:
                        sn += 1
                        detail = self.get_student_report(obj,sn)
                        output.append(detail)
                    return Response(output)

        return Response("Wrong Choice!!")

class LibraryReportViewSet(ModelViewSet):
    queryset = BookIssue.objects.all()
    serializer_class = BookIssueGetSerializer

    def list(self,request):
        output = []
        data = request.GET
        if data['report_for'] == 'issuedbook':
            objects = BookIssue.objects.filter(status=data['status'])
            for obj in objects:
                output.append(BookIssueGetSerializer(obj).data)
            return Response(output)
        else:
            objects = Book.objects.all()
            for obj in objects:
                pass

            return Response("heksh")