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
from student.models import Student,SectionStudent
class ReportViewset(viewsets.ViewSet):

    def list(self,request):
        
        userdql=['blood_group','religion','route']
        r=request.GET
        res=[] 
        lst=[]
        for k in userdql:
            print(k)
            if k in r and k != 'route':
                
                v=r.get(k)
                qr={"{}".format(k):"{}".format(v)}
                userd=UserDetail.objects.filter(**qr)
                userv=userd.values('user')
                userval=[users for users in userv]
                if userval != []:
                    print(userval)
                    for user in userval:
                        print(user)
                        vls=list(user.values())
                        usr=User.objects.get(id=vls[0])
                        print(usr)
                        stdt=Student.objects.get(user_id=usr.id)
                        print(stdt.id)
                        try:
                            stdtadm=StudentAdmission.objects.get(student_id=3)
                        except:
                            return Response('student exists but it is not admitted')    
                        bat=stdtadm.batch
                        print(bat)
                        print(r.get('batch'))
                        if bat == int(r.get('batch')):
                            print('True')
                            lst=[]
                            c=ContentType.objects.get_for_model(usr)
                            address = Address.objects.get(content_type=c,object_id=usr.id)
                            phone = Phone.objects.get(content_type=c,object_id=usr.id,type=1)
                            father = Parent.objects.get(content_type=c,object_id=usr.id,type='Father' )
                            mother = Parent.objects.get(content_type=c,object_id=usr.id,type='Mother')
                            tmp={}
                            tmp['name']  = usr.first_name+" "+usr.last_name
                            tmp['email'] = usr.email
                            tmp['address_detail'] = AddressSerializer(address).data
                            phone_data = PhoneSerializer(phone).data
                            tmp['phone'] = phone_data
                            tmp['parent_details']={
			                    'father':FatherSerializer(father).data,
			                    'mother':MotherSerializer(mother).data
			                    }
                            std=stdt
                            stdtadm=stdtadm
                            tmp['admission_date'] = stdtadm.admission_date
                            try:
                                gstd=GuardianStudent.objects.get(student_id=4)
                            except:
                                return Response('Guardian student object for the student does not exist')    

                            grd=gstd.guardian.user
                            gc=ContentType.objects.get_for_model(grd)
                            gaddress=Address.objects.get(content_type=gc,object_id=grd.id)
                            gphone=Phone.objects.get(content_type=gc,object_id=grd.id,type=1)
                            tmp['guardian_details'] = {'contact':PhoneSerializer(gphone).data,
                                                'address':AddressSerializer(gaddress).data,
                                                'name':grd.first_name+" "+grd.last_name}
                            # try:
                            #     ss=SectionStudent.objects.get(student_id=std.id)
                            # except:
                            #     return Response('Section student for student not found!')
                            # clas=ss.section._class.name
                            # tmp['class']=clas

                            lst.append(tmp)
                        else:
                            return Response ([])
                else:
                    return Response([])        
            elif k in r and k == 'route':

                v=r.get(k)
                qr={"{}".format(k):"{}".format(v)}
                print(qr)
                tstd=TransportAllocation.objects.filter(**qr)
                

                tstdv=tstd.values('student')
            
                print(tstdv)
                stdval=[std for std in tstdv]
                if stdval != []:
                    print(stdval)
                    for stds in stdval:
                        print(stds)
                        stdvals=list(stds.values())
                        stdnt=Student.objects.get(id=stdvals[0])
                        try:
                            stdntadm=StudentAdmission.objects.get(student_id=stdnt.id)
                        except:
                            return Response('Student exists but it is not admitted')    
                        bat=stdntadm.batch
                        usr=stdnt.user

                        if bat == int(r.get('batch')):
                            print('True')
                            lst=[]
                            c=ContentType.objects.get_for_model(usr)
                            address = Address.objects.get(content_type=c,object_id=usr.id)
                            phone = Phone.objects.get(content_type=c,object_id=usr.id,type=1)
                            father = Parent.objects.get(content_type=c,object_id=usr.id,type='Father' )
                            mother = Parent.objects.get(content_type=c,object_id=usr.id,type='Mother')
                            tmp={}
                            tmp['name']  = usr.first_name+" "+usr.last_name
                            tmp['email'] = usr.email
                            tmp['address_detail'] = AddressSerializer(address).data
                            phone_data = PhoneSerializer(phone).data
                            tmp['phone'] = phone_data
                            tmp['parent_details']={
			                    'father':FatherSerializer(father).data,
			                    'mother':MotherSerializer(mother).data
			                    }
                            std=stdnt
                            stdadm=stdntadm
                            tmp['admission_date'] = stdadm.admission_date
                            try:
                                gstd=GuardianStudent.objects.get(student_id=std.id)
                            except:
                                return Response('Guardian student object for this student does not exist')    
                            grd=gstd.guardian.user
                            gc=ContentType.objects.get_for_model(grd)
                            gaddress=Address.objects.get(content_type=gc,object_id=grd.id)
                            gphone=Phone.objects.get(content_type=gc,object_id=grd.id,type=1)
                            tmp['guardian_details'] = {'contact':PhoneSerializer(gphone).data,
                                                    'address':AddressSerializer(gaddress).data,
                                                    'name':grd.first_name+" "+grd.last_name}

                            lst.append(tmp)


                        else:
                            return Response ([])
            

                                
                else:
                    return Response([])
            elif k not in r and k=='gender':
                v=r.get(k)
                qr={"{}".format(k):"{}".format(v)}
                userv=User.objects.filter(**qr) 
                userval=[users for users in userv]
                if userval != []:
                    print(userval)
                    for user in userval:
                        print(user)
                        vls=list(user.values())
                        usr=User.objects.get(id=vls[0])
                        print(usr)
                        stdt=Student.objects.get(user_id=usr.id)
                        print(stdt.id)
                        try:
                            stdtadm=StudentAdmission.objects.get(student_id=3)
                        except:
                            return Response('student exists but it is not admitted')    
                        bat=stdtadm.batch
                        print(bat)
                        print(r.get('batch'))
                        if bat == int(r.get('batch')):
                            print('True')
                            lst=[]
                            c=ContentType.objects.get_for_model(usr)
                            address = Address.objects.get(content_type=c,object_id=usr.id)
                            phone = Phone.objects.get(content_type=c,object_id=usr.id,type=1)
                            father = Parent.objects.get(content_type=c,object_id=usr.id,type='Father' )
                            mother = Parent.objects.get(content_type=c,object_id=usr.id,type='Mother')
                            tmp={}
                            tmp['name']  = usr.first_name+" "+usr.last_name
                            tmp['email'] = usr.email
                            tmp['address_detail'] = AddressSerializer(address).data
                            phone_data = PhoneSerializer(phone).data
                            tmp['phone'] = phone_data
                            tmp['parent_details']={
			                    'father':FatherSerializer(father).data,
			                    'mother':MotherSerializer(mother).data
			                    }
                            std=stdt
                            stdtadm=stdtadm
                            tmp['admission_date'] = stdtadm.admission_date
                            try:
                                gstd=GuardianStudent.objects.get(student_id=4)
                            except:
                                return Response('Guardian student object for the student does not exist')    

                            grd=gstd.guardian.user
                            gc=ContentType.objects.get_for_model(grd)
                            gaddress=Address.objects.get(content_type=gc,object_id=grd.id)
                            gphone=Phone.objects.get(content_type=gc,object_id=grd.id,type=1)
                            tmp['guardian_details'] = {'contact':PhoneSerializer(gphone).data,
                                                'address':AddressSerializer(gaddress).data,
                                                'name':grd.first_name+" "+grd.last_name}
                            # try:
                            #     ss=SectionStudent.objects.get(student_id=std.id)
                            # except:
                            #     return Response('Section student for student not found!')
                            # clas=ss.section._class.name
                            # tmp['class']=clas

                            lst.append(tmp)
                        else:
                            return Response ([])        
                else:
                    return Response ([])          
            
            res=lst   
        return Response(res)

                
                               