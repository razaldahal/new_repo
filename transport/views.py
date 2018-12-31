from django.shortcuts import render
from .models import *
from .serializers import *
from rest_framework.response import Response
from rest_framework import viewsets,status
# Create your views here.
class BusStaffViewset(viewsets.ModelViewSet):
    serializer_class=BusStaffSerializer
    queryset=BusStaff.objects.all()

    def create(self,requetst):
        serializer=self.get_serializer(data=requetst.data)
        if serializer.is_valid():
            data=serializer.data
            
            c,d=BusStaff.objects.get_or_create(name=data['name'],license_no=data['license_no'],date_of_birth=data['date_of_birth'],current_address=data['current_address'],permanent_address=data['permanent_address'])
            if not d:
                return Response({'Detail':'Staff already registered!'},status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response(data,status=status.HTTP_201_CREATED)    
        else:
            raise serializers.ValidationError({'Detail':[serializer.errors]})

    def list(self,requets):
        objects=self.queryset
        output=[]
        
        for obj in objects:
            temp={'id':obj.id,
            'name':obj.name,
            'license_no':obj.license_no,
            'current_address':obj.current_address,
            'permanent_address':obj.permanent_address,
            'date_of_birth':obj.date_of_birth,
            'phone_number':obj.phone_number
            }
            # user=obj.user
            # c=ContentType.objects.get_for_model(user)
            # address=Address.objects.get(content_type=c,object_id=user.id)
            # phone=Phone.objects.get(content_type=c,object_id=user.id,type=1)

            # temp['adress']=AddressSerializer(address).data
            # temp['phone']=PhoneSerializer(phone).data
            output.append(temp)

        return Response(output)

    def retrieve(self,request,pk):
        try:
            a=BusStaff.objects.get(id=pk)
        except:
            return Response({'Detail':'Staff does not exist'},status=status.HTTP_404_NOT_FOUND)
        temp={'name':a.name,
            'license_no':a.license_no,
            'current_address':a.current_address,
            'permanent_address':a.permanent_address,
            'date_of_birth':a.date_of_birth,
            'phone_number':a.phone_number
            }
        return Response(temp)        

    def update(self,request,pk):
        try:
            a=BusStaff.objects.get(id=pk)
        except:
            return Response({'Detail':'Staff does not exist'},status=status.HTTP_404_NOT_FOUND)
        # user=a.user
        # c=ContentType.objects.get_for_model(user)
        # address=Address.objects.get(content_type=c,object_id=user.id)
        # phone=Phone.objects.get(content_type=c,object_id=user.id,type=1)

        serializer=self.get_serializer(data=request.data)
        if serializer.is_valid():
            data=serializer.data

        #     user.first_name=data['user']['first_name']
        #     user.last_name=data['user']['last_name']
        #     user.email=data['user']['email']
        #     user.gender=data['user']['gender']
        #     user.type=data['user']['type']

        #     address.province=data['address_detail']['province']
        #     address.district=data['adress_detail']['district']
        #     address.city=data['address_detail']['city']
        #     address.address=data['address_detail']['address']

        #     phone.type=data['phone_detail']['type']
        #     phone.number=data['phone_detail']['number']

            a.license_no=data['license_no']
            a.name=data['name']
            a.current_address=data['current_address']
            a.permanent_address=data['permanet_address']
            a.date_of_birth=data['date_of_birth']
            a.phone_number=data['phone_number']    


        #     user.save()
        #     address.save()
        #     phone.save()
            a.save()
            return Response(data)
        else:
            return Response(serializer.errors)    




class TransportViewSet(viewsets.ModelViewSet):
    serializer_class=TransportSerializer
    queryset=Transport.objects.all()
    def create(self,request):
        serializer=self.get_serializer(data=request.data)
        if serializer.is_valid():
            data=serializer.data
            a,b=Transport.objects.get_or_create(vehicle_no=data['vehicle_no'],driver=BusStaff.objects.get(id=data['driver']),
            #route=Route.objects.get(id=data['route']),
            no_of_seats=data['no_of_seats'],
            max_allowed=data['max_allowed'],
            insurance_renew_date=data['insurance_renew_date'],
            contact_person=data['contact_person']
            )
            if not b:
                return Response({'Detail':'Already Registered!'},status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response(data,status=status.HTTP_201_CREATED)
        else:
            raise serializers.ValidationError ({'Detail':[serializer.errors]})
    def list(self,requets):
        objects=self.queryset
        output=[]
        

        for obj in objects:
            temp={'id':obj.id,
            'vehicle_no':obj.vehicle_no,
            'driver':obj.driver.name,
            #'start_location':obj.route.start_location,
            #'stop_location':obj.route.stop_location,
            'no_of_seats':obj.no_of_seats,
            'max_allowed':obj.max_allowed,
            'insurance_renew_date':obj.insurance_renew_date,
            'contact_person':obj.contact_person
            }
            # user=obj.contact_person
            # c=ContentType.objects.get_for_model(user)
            # phone=Phone.objects.get(content_type=c,object_id=user.id,type=1)
            # temp['contact_no']=phone.number
            output.append(temp)

        return Response(output)        

class RouteViewSet(viewsets.ModelViewSet):
    queryset=Route.objects.all()
    serializer_class=RouteSerializer

    def create(self,request):
        serializer=self.get_serializer(data=request.data)
        if serializer.is_valid():
            data=serializer.data
            a,b=Route.objects.get_or_create(start_location=data['start_location'],stop_location=data['stop_location'],start_time=data['start_time'],fee_amount=data['fee_amount'])
            if not b:
                return Response({'Detail':'Already added!'},status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response(data,status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors)

    def list(self,request):
        objects=self.queryset
        output=[]
        for obj in objects:
            temp={'id':obj.id,
            'start_location':obj.start_location,
            'stop_location':obj.stop_location,
            'start_time':obj.start_time,
            'fee_amount':obj.fee_amount
            }
            output.append(temp)
        return Response(output)   

    def update(self,request,pk):
        a=Route.objects.get(id=pk)
        serializer=self.get_serializer(data=request.data)
        if serializer.is_valid():
            data=serializer.data

            a.start_location=data['start_location']
            a.stop_location=data['stop_location']
            a.start_time=data['start_time']
            a.fee_amount=data['fee_amount']
            a.save()
            return Response(data)
        else:
            return Response(serializer.errors)

class TransportAllocationViewSet(viewsets.ModelViewSet):
    serializer_class=TransportAllocationSerializer
    queryset=TransportAllocation.objects.all()

    def create(self,request):
        serializer=self.get_serializer(data=request.data)
        if serializer.is_valid():
            data=serializer.data
            a,b=TransportAllocation.objects.get_or_create(batch=Batch.objects.get(id=data['batch']),course=Course.objects.get(id=data['course']),_class=Class.objects.get(id=data['_class']),section=Section.objects.get(id=data['section']),student=Student.objects.get(id=data['student']),route=Route.objects.get(id=data['route']))
            if not b:
                return Response({'Detail':'Alreday Added!'},status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response(data,status=status.HTTP_201_CREATED)
        else:
            return Response({'Detail':[serializer.errors]})

    def list(self,request):
        objects=self.queryset
        output=[]
        for obj in objects:
            temp={'id':obj.id,
            'batch':obj.batch.name,
            'course':obj.course.name,
            'route':obj.route.start_location+" "+obj.route.stop_location,
            'class':obj._class.name,
            'section':obj.section.name,
            'student':obj.student.user.first_name+" "+obj.student.user.last_name
            }            
            output.append(temp)
        return Response(output)

    def retrieve(self,requets,pk):
        try:
            t=TransportAllocation.objects.get(id=pk)
        except:
            return Response({'Detail':'Object not Found'},status=status.HTTP_404_NOT_FOUND)
        temp={'batch':t.batch.name,
            'course':t.course.name,
            'route':t.route.start_location+" "+t.route.stop_location,
            'class':t._class.name,
            'section':t.section.name,
            'student':t.student.user.first_name+" "+t.student.user.last_name
            }
        return Response(temp)



