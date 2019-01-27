from django.shortcuts import render
from rest_framework import viewsets,status
from rest_framework.response import Response
from rest_framework import generics,filters
from rest_framework.views import APIView
from admission.serializers import *
from django.contrib.contenttypes.models import ContentType
# Create your views here.
from main.models import User,UserDetail,Address,Phone,Parent
from transport.models import Route,TransportAllocation
from admission.models import StudentAdmission
from guardian.models import Guardian,GuardianStudent
from student.models import Student
class ReportViewset(viewsets.ViewSet):

    def list(self,request):
        
        userdql=['blood_group','gender','religion']
        res=[]
        for k in userdql:
            if k in request.GET:
                
                v=request.GET.get(k)
                qr={"{}".format(k):"{}".format(v)}
                userd=UserDetail.objects.filter(**qr)
                userval=userd.values('user')
                
                for user in userval:
                    usr=User.objects.get(**user)
                    stdt=Student.objects.get(user_id=usr.id)
                    stdtadm=StudentAdmission.objects.get(student_id=stdt.id)
                    bat=stdtadm.batch
                    
                    if bat == request.GET.get('batch'):
                        lst=[]
                        c=ContentType.objects.get_for_model(usr)
                        address = Address.objects.get(content_type=c,object_id=usr.id)
                        phone = Phone.objects.get(content_type=c,object_id=usr.id,type=1)
                        father = Parent.objects.get(content_type=c,object_id=usr.id,type='Father' )
                        mother = Parent.objects.get(content_type=c,object_id=usr.id,type='Mother')
                        tmp={}
                        tmp['user']  = usr.first_name+" "+usr.last_name
                        tmp['email'] = usr.email
                        tmp['address_detail'] = AddressSerializer(address).data
                        phone_data = PhoneSerializer(phone).data
                        tmp['phone'] = phone_data
                        tmp['parent_details']={
			                'father':FatherSerializer(father).data,
			                'mother':MotherSerializer(mother).data
			                }
                        std=Student.objects.get(user_id=usr.id)
                        stdadm=StudentAdmission.objects.get(student_id=std.id)
                        tmp['admission_date'] = stdadm.admission_date
                        gstd=GuardianStudent.objects.get(student_id=std.id)
                        grd=gstd.guardian.user
                        gc=ContentType.objects.get_for_model(grd)
                        gaddress=Address.objects.get(content_type=gc,object_id=grd.id)
                        gphone=Phone.objects.get(content_type=gc,object_id=grd.id,type=1)
                        tmp['guardian_details'] = {'contact':PhoneSerializer(gphone).data,
                                                'address':AddressSerializer(gaddress).data,
                                                'name':grd.user.first_name+" "+grd.user.last_name}

                        lst.append(tmp)
                        
                    
                    else:
                        return Response('No matching result!')  
                    res=lst   
        return Response(res)

                
                               