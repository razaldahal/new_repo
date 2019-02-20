from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework import generics, filters
from rest_framework.views import APIView
from admission.serializers import *
from django.contrib.contenttypes.models import ContentType
# Create your views here.
from main.models import User, UserDetail, Address, Phone, Parent
from transport.models import Route, TransportAllocation
from admission.models import StudentAdmission
from guardian.models import Guardian, GuardianStudent
from student.models import Student, SectionStudent


class ReportViewset(viewsets.ViewSet):

    def list(self, request):
        print(request.GET)
        userdql = ['blood_group', 'religion', 'route']
        r = request.GET
        res = []
        lst = []
        
        for k in userdql:
            print(k)
            if k in r and k != 'route':

                v = r.get(k)
                qr = {"{}".format(k): "{}".format(v)}
                userd = UserDetail.objects.filter(**qr)
                userv = userd.values('user')
                userval = [users for users in userv]
                if userval != []:
                    print(userval)
                    id=0
                    for user in userval:
                        id=id
                        print(user)

                        vls = list(user.values())
                        usr = User.objects.get(id=vls[0])
                        print(usr)
                        try:
                            stdt = Student.objects.get(user_id=usr.id)
                        except:
                            continue    
                        print(stdt.id)
                        try:
                            stdtadm = StudentAdmission.objects.get(
                                student_id=stdt.id)
                        except:
                            return Response('student exists but it is not admitted')
                        bat = stdtadm.batch
                        _class = SectionStudent.objects.get(student_id=stdt.id).section._class
                        if _class.name == str(r.get('class')):
                        
                            print('True')
                            lst = []
                            c = ContentType.objects.get_for_model(usr)
                            address = Address.objects.get(
                                content_type=c, object_id=usr.id)
                            phone = Phone.objects.get(
                                content_type=c, object_id=usr.id, type=1)
                            father = Parent.objects.get(
                                content_type=c, object_id=usr.id, type='Father')
                            mother = Parent.objects.get(
                                content_type=c, object_id=usr.id, type='Mother')
                            tmp = {}
                            tmp['name'] = usr.first_name+" "+usr.last_name
                            tmp['email'] = usr.email
                            tmp['address_detail'] = AddressSerializer(
                                address).data
                            phone_data = PhoneSerializer(phone).data
                            tmp['phone'] = phone_data
                            tmp['parent_details'] = {
                                'father': FatherSerializer(father).data,
         			                    'mother': MotherSerializer(mother).data
                            }
                            std = stdt
                            stdtadm = stdtadm
                            tmp['admission_no']=std.registration_no
                            tmp['batch']=stdtadm.batch
                            tmp['course']=stdtadm.course.name
                            tmp['admission_date'] = stdtadm.admission_date
                            tmp['id']=id+1
                            id+=1 
                            try:
                                gstd = GuardianStudent.objects.get(
                                    student_id=std.id)
                            except:
                                return Response('Guardian student object for the student does not exist')

                            grd = gstd.guardian.user
                            gc = ContentType.objects.get_for_model(grd)
                            gaddress = Address.objects.get(
                                content_type=gc, object_id=grd.id)
                            gphone = Phone.objects.get(
                                content_type=gc, object_id=grd.id, type=1)
                            tmp['guardian_details'] = {'contact': PhoneSerializer(gphone).data,
                                                       'address': AddressSerializer(gaddress).data,
                                                       'name': grd.first_name+" "+grd.last_name}
                            # try:
                            #     ss=SectionStudent.objects.get(student_id=std.id)
                            # except:
                            #     return Response('Section student for student not found!')
                            # clas=ss.section._class.name
                            # tmp['class']=clas

                            lst.append(tmp)
                        elif not r.get('class'):

                            id=id                        
                            print('True')
                            lst = []
                            c = ContentType.objects.get_for_model(usr)
                            address = Address.objects.get(
                                content_type=c, object_id=usr.id)
                            phone = Phone.objects.get(
                                content_type=c, object_id=usr.id, type=1)
                            father = Parent.objects.get(
                                content_type=c, object_id=usr.id, type='Father')
                            mother = Parent.objects.get(
                                content_type=c, object_id=usr.id, type='Mother')
                            tmp = {}
                            tmp['name'] = usr.first_name+" "+usr.last_name
                            tmp['email'] = usr.email
                            tmp['address_detail'] = AddressSerializer(
                                address).data
                            phone_data = PhoneSerializer(phone).data
                            tmp['phone'] = phone_data
                            tmp['parent_details'] = {
                                'father': FatherSerializer(father).data,
         			                    'mother': MotherSerializer(mother).data
                            }
                            std = stdt
                            stdtadm = stdtadm
                            tmp['batch']=stdtadm.batch
                            tmp['course']=stdtadm.course.name                            
                            tmp['admission_no']=std.registration_no
                            tmp['admission_date'] = stdtadm.admission_date
                            tmp['id']=id+1
                            id+=1
                            try:
                                gstd = GuardianStudent.objects.get(
                                    student_id=std.id)
                            except:
                                return Response('Guardian student object for the student does not exist')

                            grd = gstd.guardian.user
                            gc = ContentType.objects.get_for_model(grd)
                            gaddress = Address.objects.get(
                                content_type=gc, object_id=grd.id)
                            gphone = Phone.objects.get(
                                content_type=gc, object_id=grd.id, type=1)
                            tmp['guardian_details'] = {'contact': PhoneSerializer(gphone).data,
                                                       'address': AddressSerializer(gaddress).data,
                                                       'name': grd.first_name+" "+grd.last_name}
                            lst.append(tmp)
                        elif _class.name!=str(r.get('class')):
                            return Response([])        
                else:
                    return Response([])
            elif k in r and k == 'route':

                v = r.get(k)
                qr = {"{}".format(k): "{}".format(v)}
                print(qr)
                tstd = TransportAllocation.objects.filter(**qr)

                tstdv = tstd.values('student')

                print(tstdv)
                stdval = [std for std in tstdv]
                if stdval != []:
                    print(stdval)
                    id=0
                    for stds in stdval:
                        id=id
                        print(stds)
                        stdvals = list(stds.values())
                        stdnt = Student.objects.get(id=stdvals[0])
                        print(stdnt)
                        try:
                            stdntadm = StudentAdmission.objects.get(
                                student_id=stdnt.id)
                        except:
                            return Response('Student exists but it is not admitted')
                        bat = stdntadm.batch
                        usr = stdnt.user
                        _class = SectionStudent.objects.get(student_id=stdt.id).section._class
                        print(bat)
                        print(r.get('batch'))
                        if _class.name == str(r.get('class')):
                            print('True')
                            lst = []
                            c = ContentType.objects.get_for_model(usr)
                            address = Address.objects.get(
                                content_type=c, object_id=usr.id)
                            phone = Phone.objects.get(
                                content_type=c, object_id=usr.id, type=1)
                            father = Parent.objects.get(
                                content_type=c, object_id=usr.id, type='Father')
                            mother = Parent.objects.get(
                                content_type=c, object_id=usr.id, type='Mother')
                            tmp = {}
                            tmp['name'] = usr.first_name+" "+usr.last_name
                            tmp['email'] = usr.email
                            tmp['address_detail'] = AddressSerializer(
                                address).data
                            phone_data = PhoneSerializer(phone).data
                            tmp['phone'] = phone_data
                            tmp['parent_details'] = {
                                'father': FatherSerializer(father).data,
         			                    'mother': MotherSerializer(mother).data
                            }
                            std = stdnt
                            stdadm = stdntadm
                            tmp['batch']=stdtadm.batch
                            tmp['course']=stdtadm.course.name                            
                            tmp['admission_no']=std.registration_no
                            tmp['admission_date'] = stdadm.admission_date
                            tmp['id']=id+1
                            try:
                                gstd = GuardianStudent.objects.get(
                                    student_id=std.id)
                            except:
                                return Response('Guardian student object for this student does not exist')
                            grd = gstd.guardian.user
                            gc = ContentType.objects.get_for_model(grd)
                            gaddress = Address.objects.get(
                                content_type=gc, object_id=grd.id)
                            gphone = Phone.objects.get(
                                content_type=gc, object_id=grd.id, type=1)
                            tmp['guardian_details'] = {'contact': PhoneSerializer(gphone).data,
                                                       'address': AddressSerializer(gaddress).data,
                                                       'name': grd.first_name+" "+grd.last_name}

                            lst.append(tmp)

                        elif not r.get('class'):
                            id=id                        
                            print('True')
                            lst = []
                            c = ContentType.objects.get_for_model(usr)
                            address = Address.objects.get(
                                content_type=c, object_id=usr.id)
                            phone = Phone.objects.get(
                                content_type=c, object_id=usr.id, type=1)
                            father = Parent.objects.get(
                                content_type=c, object_id=usr.id, type='Father')
                            mother = Parent.objects.get(
                                content_type=c, object_id=usr.id, type='Mother')
                            tmp = {}
                            tmp['name'] = usr.first_name+" "+usr.last_name
                            tmp['email'] = usr.email
                            tmp['address_detail'] = AddressSerializer(
                                address).data
                            phone_data = PhoneSerializer(phone).data
                            tmp['phone'] = phone_data
                            tmp['parent_details'] = {
                                'father': FatherSerializer(father).data,
         			                    'mother': MotherSerializer(mother).data
                            }
                            std = stdt
                            stdtadm = stdtadm
                            tmp['batch']=stdtadm.batch
                            tmp['course']=stdtadm.course.name                           
                            tmp['admission_no']=std.registration_no
                            tmp['admission_date'] = stdtadm.admission_date
                            tmp['id']=id+1
                            try:
                                gstd = GuardianStudent.objects.get(
                                    student_id=std.id)
                            except:
                                return Response('Guardian student object for the student does not exist')

                            grd = gstd.guardian.user
                            gc = ContentType.objects.get_for_model(grd)
                            gaddress = Address.objects.get(
                                content_type=gc, object_id=grd.id)
                            gphone = Phone.objects.get(
                                content_type=gc, object_id=grd.id, type=1)
                            tmp['guardian_details'] = {'contact': PhoneSerializer(gphone).data,
                                                       'address': AddressSerializer(gaddress).data,
                                                       'name': grd.first_name+" "+grd.last_name}
                            lst.append(tmp)
                        elif _class.name!=str(r.get('class')):
                            return Response([])

                else:
                    return Response([])
            elif k not in r and 'gender' in r:
                k='gender'
                v = r.get(k)
                qr = {"{}".format(k): "{}".format(v)}
                userv = User.objects.filter(**qr)
                userval = [users for users in userv]
                if userval != []:
                    print(userval)
                    id=0
                    for user in userval:
                        print(user)
                        id=id
                        usr = User.objects.get(id=user.id)
                        print(usr)
                        try: 
                            stdt = Student.objects.get(user_id=usr.id)
                        except:
                            continue    
                        print(stdt.id)
                        try:
                            stdtadm = StudentAdmission.objects.get(
                                student_id=stdt.id)
                        except:
                            return Response('student exists but it is not admitted')
                        bat = stdtadm.batch
                        print(bat)
                        print(r.get('batch'))
                        _class = SectionStudent.objects.get(student_id=stdt.id).section._class
                        print(bat)
                        print(r.get('batch'))
                        if _class.name == str(r.get('class')):
                            print('True')
                            lst = []
                            c = ContentType.objects.get_for_model(usr)
                            address = Address.objects.get(
                                content_type=c, object_id=usr.id)
                            phone = Phone.objects.get(
                                content_type=c, object_id=usr.id, type=1)
                            father = Parent.objects.get(
                                content_type=c, object_id=usr.id, type='Father')
                            mother = Parent.objects.get(
                                content_type=c, object_id=usr.id, type='Mother')
                            tmp = {}
                            tmp['name'] = usr.first_name+" "+usr.last_name
                            tmp['email'] = usr.email
                            tmp['address_detail'] = AddressSerializer(
                                address).data
                            phone_data = PhoneSerializer(phone).data
                            tmp['phone'] = phone_data
                            tmp['parent_details'] = {
                                'father': FatherSerializer(father).data,
         			                    'mother': MotherSerializer(mother).data
                            }
                            std = stdt
                            stdtadm = stdtadm
                            tmp['batch']=stdtadm.batch
                            tmp['course']=stdtadm.course.name                            
                            tmp['admission_no']=std.registration_no
                            tmp['admission_date'] = stdtadm.admission_date
                            tmp['id']=id+1
                            id+=1
                            try:
                                gstd = GuardianStudent.objects.get(
                                    student_id=std.id)
                            except:
                                return Response('Guardian student object for the student does not exist')

                            grd = gstd.guardian.user
                            gc = ContentType.objects.get_for_model(grd)
                            gaddress = Address.objects.get(
                                content_type=gc, object_id=grd.id)
                            gphone = Phone.objects.get(
                                content_type=gc, object_id=grd.id, type=1)
                            tmp['guardian_details'] = {'contact': PhoneSerializer(gphone).data,
                                                       'address': AddressSerializer(gaddress).data,
                                                       'name': grd.first_name+" "+grd.last_name}
                            # try:
                            #     ss=SectionStudent.objects.get(student_id=std.id)
                            # except:
                            #     return Response('Section student for student not found!')
                            # clas=ss.section._class.name
                            # tmp['class']=clas

                            lst.append(tmp)
                        elif not r.get('class'):                        
                            id=id                        
                            print('True')
                            lst = []
                            c = ContentType.objects.get_for_model(usr)
                            address = Address.objects.get(
                                content_type=c, object_id=usr.id)
                            phone = Phone.objects.get(
                                content_type=c, object_id=usr.id, type=1)
                            father = Parent.objects.get(
                                content_type=c, object_id=usr.id, type='Father')
                            mother = Parent.objects.get(
                                content_type=c, object_id=usr.id, type='Mother')
                            tmp = {}
                            tmp['name'] = usr.first_name+" "+usr.last_name
                            tmp['email'] = usr.email
                            tmp['address_detail'] = AddressSerializer(
                                address).data
                            phone_data = PhoneSerializer(phone).data
                            tmp['phone'] = phone_data
                            tmp['parent_details'] = {
                                'father': FatherSerializer(father).data,
         			                    'mother': MotherSerializer(mother).data
                            }
                            std = stdt
                            stdtadm = stdtadm
                            tmp['batch']=stdtadm.batch
                            tmp['course']=stdtadm.course.name                            
                            tmp['admission_no']=std.registration_no
                            tmp['id'] = id+1
                            id+=1
                            tmp['admission_date'] = stdtadm.admission_date
                            try:
                                gstd = GuardianStudent.objects.get(
                                    student_id=std.id)
                            except:
                                return Response('Guardian student object for the student does not exist')

                            grd = gstd.guardian.user
                            gc = ContentType.objects.get_for_model(grd)
                            gaddress = Address.objects.get(
                                content_type=gc, object_id=grd.id)
                            gphone = Phone.objects.get(
                                content_type=gc, object_id=grd.id, type=1)
                            tmp['guardian_details'] = {'contact': PhoneSerializer(gphone).data,
                                                       'address': AddressSerializer(gaddress).data,
                                                       'name': grd.first_name+" "+grd.last_name}
                            lst.append(tmp)
                        elif _class.name!=str(r.get('class')):
                            return Response([])    
                else:
                    return Response([])

            elif k not in r and 'province' in r:
                k='province'
                print(k)                
                v = r.get(k)

                qr = {"{}".format(k): "{}".format(v)}
                addv = Address.objects.filter(**qr)
                for obj in addv:
                    user_ids = [obj.object_id]
                    if user_ids != []:
                        id=o
                        for user in user_ids:
                            print(user)
                            id=id

                            usr = User.objects.get(id=user)
                            print(usr)
                            try:    
                                stdt = Student.objects.get(user_id=usr.id)
                            except:
                                continue
                            print(stdt.id)
                            try:
                                stdtadm = StudentAdmission.objects.get(
                                    student_id=stdt.id)
                            except:
                                #return Response('student exists but it is not admitted')
                                continue
                            bat = stdtadm.batch
                            print(bat)
                            print(r.get('batch'))
                            _class = SectionStudent.objects.get(student_id=stdt.id).section._class
                            print(bat)
                            print(r.get('batch'))
                            if _class.name == str(r.get('class')):
                            
                                print('True')
                                lst = []
                                c = ContentType.objects.get_for_model(usr)
                                address = Address.objects.get(
                                    content_type=c, object_id=usr.id)
                                phone = Phone.objects.get(
                                    content_type=c, object_id=usr.id, type=1)
                                father = Parent.objects.get(
                                    content_type=c, object_id=usr.id, type='Father')
                                mother = Parent.objects.get(
                                    content_type=c, object_id=usr.id, type='Mother')
                                tmp = {}
                                tmp['name'] = usr.first_name+" "+usr.last_name
                                tmp['email'] = usr.email
                                tmp['address_detail'] = AddressSerializer(
                                    address).data
                                phone_data = PhoneSerializer(phone).data
                                tmp['phone'] = phone_data
                                tmp['parent_details'] = {
                                    'father': FatherSerializer(father).data,
         			                    'mother': MotherSerializer(mother).data
                                    }
                                std = stdt
                                stdtadm = stdtadm
                                tmp['batch']=stdtadm.batch
                                tmp['course']=stdtadm.course.name                                
                                tmp['admission_no']=std.registration_no
                                tmp['admission_date'] = stdtadm.admission_date
                                tmp['id']=id+1
                                id+=1
                                try:
                                    gstd = GuardianStudent.objects.get(
                                        student_id=std.id)
                                except:
                                    return Response('Guardian student object for the student does not exist')
                                print(gstd)
                                grd = gstd.guardian.user
                                gc = ContentType.objects.get_for_model(grd)
                                gaddress = Address.objects.get(
                                    content_type=gc, object_id=grd.id)
                                gphone = Phone.objects.get(
                                    content_type=gc, object_id=grd.id, type=1)
                                tmp['guardian_details'] = {'contact': PhoneSerializer(gphone).data,
                                                       'address': AddressSerializer(gaddress).data,
                                                       'name': grd.first_name+" "+grd.last_name}
                            # try:
                            #     ss=SectionStudent.objects.get(student_id=std.id)
                            # except:
                            #     return Response('Section student for student not found!')
                            # clas=ss.section._class.name
                            # tmp['class']=clas

                                lst.append(tmp)
                            elif not r.get('class'):                        

                                id=id                        
                                print('True')
                                lst = []
                                c = ContentType.objects.get_for_model(usr)
                                address = Address.objects.get(
                                    content_type=c, object_id=usr.id)
                                phone = Phone.objects.get(
                                    content_type=c, object_id=usr.id, type=1)
                                father = Parent.objects.get(
                                    content_type=c, object_id=usr.id, type='Father')
                                mother = Parent.objects.get(
                                    content_type=c, object_id=usr.id, type='Mother')
                                tmp = {}
                                tmp['name'] = usr.first_name+" "+usr.last_name
                                tmp['email'] = usr.email
                                tmp['address_detail'] = AddressSerializer(
                                    address).data
                                phone_data = PhoneSerializer(phone).data
                                tmp['phone'] = phone_data
                                tmp['parent_details'] = {
                                    'father': FatherSerializer(father).data,
         			                'mother': MotherSerializer(mother).data
                                    }
                                std = stdt
                                stdtadm = stdtadm
                                tmp['batch']=stdtadm.batch
                                tmp['course']=stdtadm.course.name
                                tmp['admission_no']=std.registration_no
                                tmp['id']=id+1
                                id+=1
                                tmp['admission_date'] = stdtadm.admission_date
                                try:
                                    gstd = GuardianStudent.objects.get(
                                        student_id=std.id)
                                except:
                                    return Response('Guardian student object for the student does not exist')

                                grd = gstd.guardian.user
                                gc = ContentType.objects.get_for_model(grd)
                                gaddress = Address.objects.get(
                                    content_type=gc, object_id=grd.id)
                                gphone = Phone.objects.get(
                                    content_type=gc, object_id=grd.id, type=1)
                                tmp['guardian_details'] = {'contact': PhoneSerializer(gphone).data,
                                                        'address': AddressSerializer(gaddress).data,
                                                        'name': grd.first_name+" "+grd.last_name}
                                lst.append(tmp)
                            elif _class.name!=str(r.get('class')):
                                return Response([])                            
                    else:
                        return Response([])

            res = lst
        return Response(res)
