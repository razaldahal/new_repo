from rest_framework import viewsets,serializers,status
from rest_framework.response import Response
from num2words import num2words
from datetime import datetime
from operator import itemgetter


from .serializers import *
from .models import *

class ExpenseCategoryViewSet(viewsets.ModelViewSet):
    queryset = ExpenseCategory.objects.all()
    serializer_class = ExpenseCategorySerializer

class DailyExpenseViewSet(viewsets.ViewSet):
    queryset = DailyExpense.objects.all()

    def create(self,request):
        serializer = DailyExpenseSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.data
            print(data)
            obj  = DailyExpense.objects.create(expense_type_id = data['expense_type'],
                    expense_detail = data['expense_detail'],
                    amount = data['amount'],
                    expense_date = data['expense_date'],
                    receipt_number = data['receipt_number']
            )
           
            return Response(data,status=status.HTTP_201_CREATED)
        else:
            raise serializers.ValidationError(
                {'Detail':[serializer.errors]}
            )

    def list(self,request):
        objects = self.queryset
        output = []
        data = request.GET
        # print(data)
        # print(type(data))
        try:
            expense_category = data['expense_category']
            expense_category = int(expense_category)
            if expense_category == 0:
                objects = self.queryset
                for obj in objects:
                    temp ={
                        'id':obj.id,
                        'expense_type':obj.expense_type.name,
                        'amount':obj.amount,
                        'expense_date':obj.expense_date,
                        }
                    output.append(temp)
            else:
                objects = self.queryset.filter(expense_type_id=expense_category)
                for obj in objects:
                    temp ={
                            'id':obj.id,
                            'expense_type':obj.expense_type.name,
                            'amount':obj.amount,
                            'expense_date':obj.expense_date,
                            
                        }
                    output.append(temp)
        except:
            objects = self.queryset.filter(expense_date__range=[data['start_date'],data['end_date']])
            for obj in objects:
                temp ={
                        'id':obj.id,
                        'expense_type':obj.expense_type.name,
                        'amount':obj.amount,
                        'expense_date':obj.expense_date,
                        
                    }
                output.append(temp)

        return Response(output,status=status.HTTP_200_OK)

    def get_object(self,pk):
        return DailyExpense.objects.get(id = pk)

    def retrieve(self,request,pk):
        obj = self.get_object(pk)
        temp ={
            'id':obj.id,
            'expense_type':obj.expense_type.id,
            'amount':obj.amount,
            'expense_date':obj.expense_date,
            'expense_detail':obj.expense_detail,
            'receipt_number':obj.receipt_number,
            
        }
        return Response(temp,status=status.HTTP_200_OK)

    def update(self,request,pk):
        obj = self.get_object(pk)
        serializer = DailyExpenseSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.data
            # print(data)
            obj.expense_type_id = data.get('expense_type',obj.expense_type)
            obj.expense_detail = data.get('expense_detail',obj.expense_detail)
            obj.amount = data.get('amount',obj.amount)
            obj.expense_date = data.get('expense_date',obj.expense_date)
            obj.receipt_number = data.get('receipt_number',obj.receipt_number)
            obj.save()

            return Response(data,status=status.HTTP_201_CREATED)
        raise serializers.ValidationError({
            "detail":[serializer.errors]
        })

    
class FeeCategoryViewSet(viewsets.ModelViewSet):
    queryset = FeeCategory.objects.all()
    serializer_class = FeeCategorySerializer

class FeeAllocationViewSet(viewsets.ViewSet):
    queryset = FeeAllocation.objects.all()

    def create(self,request):
        serializer = FeeAllocationSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.data
            fee_for = data['fee_for']

            if fee_for == 1:
                class_obj = Class.objects.all()
                
                for c_obj in class_obj:
                    class_id = c_obj.id
                    c_filter = FeeAllocation.objects.filter(_class_id=class_id,fee_category_id=data['fee_category'])
                    if not c_filter:
                        obj,created = FeeAllocation.objects.get_or_create(fee_category_id=data['fee_category'],
                                                                _class_id =class_id,
                                                                defaults = {
                                                                    'total_amount':data['total_amount']
                                                                })
                   
                        # if not created:
                        #     return Response("Class Already Existttrfy",status=status.HTTP_400_BAD_REQUEST)
                        # if created:
                        #     return Response(data,status=status.HTTP_201_CREATED)
                        
                    if c_filter:
                        print(class_id)
                return Response(data,status=status.HTTP_201_CREATED)

            if fee_for==2:
                obj,created = FeeAllocation.objects.get_or_create(fee_category_id=data['fee_category'],
                                                            _class_id = data['_class'],
                                                            defaults = {
                                                                'total_amount':data['total_amount']
                                                            })
                if not created:
                    return Response("Fee Category & Class Should be Unique",status=status.HTTP_400_BAD_REQUEST)

                if created:
                    return Response(data,status=status.HTTP_201_CREATED)
            

           
        else:
            raise serializers.ValidationError({
                'Detail':[serializer.errors]
            })

    def get_object(self,pk):
        try:
            return FeeAllocation.objects.get(id=pk)
        except:
            raise serializers.ValidationError({
                'DataBase Error':['Data Not Exist With This Id']
            })

    def retrieve(self,request,pk):
        obj = self.get_object(pk)
        temp ={
            'id':obj.id,
            'course':obj._class.course.name,
            'class':obj._class.name,
            'fee_category':obj.fee_category.name,
            'total_amount':obj.total_amount,
         
            }
        return Response(temp,status=status.HTTP_200_OK)

    def update(self,request,pk):
        obj = self.get_object(pk)
        serializer = FeeAllocationUpdateSerializer(data=request.data)

        if serializer.is_valid():
            data = serializer.data
            obj.total_amount = data.get('total_amount',obj.total_amount)
            obj.save()
            return Response(data)
        else:
            raise serializers.ValidationError({
                'Detail':[serializer.errors]
            })
            




    def list(self,request):
        queryset = self.queryset
        output = []
        for q in queryset:
            temp ={
                'id':q.id,
                'course':q._class.course.name,
                'class':q._class.name,
                'fee_category':q.fee_category.name,
                'total_amount':q.total_amount,
                'paid_amount':0
            }
            output.append(temp)


        return Response(output,status=status.HTTP_200_OK)

class FeeCollectionViewSet(viewsets.ViewSet):
    queryset = StudentPayment.objects.all()

    def create(self,request):
        serializer = StudentPaymentSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.data
            paid_amount = int(data['amount'])
            try:
                obj = FeeAllocation.objects.get(id=data['fee_allocation_id'])
                total_amount = obj.total_amount
                
            except:
                raise serializers.ValidationError({
                    'Detail':['FeeAllocation With This Id Not Exist']
                })
            if total_amount > paid_amount:
                obj = StudentPayment.objects.create(
                            fee_allocation_id = data['fee_allocation_id'],
                            student_id = data['student_id'],
                            remarks = data['remarks'],
                            amount = data['amount'],
                            payment_status = 2,
                            payment_type = 2
                            )

            elif total_amount == paid_amount:
                obj = StudentPayment.objects.create(
                            fee_allocation_id = data['fee_allocation_id'],
                            student_id = data['student_id'],
                            remarks = data['remarks'],
                            amount = data['amount'],
                            payment_status = 1,
                            payment_type = 2
                            )

            else:
                obj = StudentPayment.objects.create(
                            fee_allocation_id = data['fee_allocation_id'],
                            student_id = data['student_id'],
                            remarks = data['remarks'],
                            amount = data['amount'],
                            payment_status = 3,
                            payment_type = 2
                        )
            
            return Response(data ,status=status.HTTP_201_CREATED)
        else:
            raise serializers.ValidationError({
                'Detail':[serializer.errors]
            })
class PaymentHistoryViewSet(viewsets.ViewSet):
    queryset = StudentPayment.objects.all()
    fclst = []
    remaining_dues = 0
    total_balance = 0
    output = []
    def PaymentStateMentDetail(self,temp):

        # newlist = sorted(dataList, key=itemgetter('paid_date'),reverse=False)
        # print(temp['paid_amount'])
        pa = temp['paid_amount']
        da = temp['dues']

        if temp['payment_type'] ==1:
            pass

       
        if temp['fee_category_id'] not in self.fclst:
            self.fclst.append(temp['fee_category_id'])
        else:
            pass
            # if pa < da:
            #     if pa == 0:
            #         # self.remaining_dues += da
            #         if self.total_balance > self.remaining_dues:
            #             self.remaining_dues += 0
            #             self.total_balance = self.total_balance - da 
            #     else:
            #         if self.total_balance > 0:
            #             if da > self.total_balance:
            #                 self.remaining_dues =da - self.total_balance
            #                 self.total_balance = 0
            #             else:
            #                 self.remaining_dues = self.total_balance - da
            #                 self.total_balance -= da
            #         else:
            #             self.remaining_dues += da - pa
            # else:
        #         if self.remaining_dues > pa:
        #             self.remaining_dues += da
        #             self.remaining_dues -= pa
        #         elif pa == 0:
        #             if self.total_balance > self.remaining_dues:
        #                 self.remaining_dues += 0
        #                 self.total_balance = self.total_balance - da 
        #         else:
        #             self.total_balance += pa - da

        #     # elif temp['']

                
        # else:
        #     if self.remaining_dues == 0:
        #         # self.total_balance +=pa
        #         if self.total_balance > da:
        #             self.total_balance -= da
        #         else:
        #             self.remaining_dues += da - self.total_balance
        #             self.total_balance = 0
        #     else:
        #         if da >pa:
        #             if pa ==0:
        #                 self.remaining_dues = self.remaining_dues + da
        #             else:
        #                 self.remaining_dues -= pa
        #         else:
        #             pass
            # self.remaining_dues = self.remaining_dues + da
            # print('remaining Amount',self.remaining_dues)
            # if self.remaining_dues >= pa:
            #     self.remaining_dues += da
            # else:
            #     self.total_balance += pa -self.remaining_dues
            #     self.remaining_dues = 0
                
            


    def list(self,request):
        queryset = self.queryset
        data = request.GET
        student_id = data['student_id']
        objects = StudentPayment.objects.filter(student_id=student_id).order_by('-date_created')
        self.output = []
        self.fclst = []
        # payment_history = {}
        for obj in objects:
            temp = {
                'paid_date':obj.date_created.strftime(('%m/%d/%Y %a,%H:%M %p')),
                'fee_category':obj.fee_allocation.fee_category.name,
                'fee_category_id':obj.fee_allocation.fee_category.id,
                'dues':obj.fee_allocation.total_amount,
                'paid_amount':obj.amount,
                'payment_status':obj.payment_status,
                'payment_type':obj.payment_type,
                }
            self.PaymentStateMentDetail(temp)
            temp['remaining_dues'] = self.remaining_dues
            temp['total_balance'] = self.total_balance
            self.output.append(temp)
            
        # payment_history['payment_history'] = output
       
        # newlist = sorted(output, key=itemgetter('paid_date'),reverse=True)
        return Response(self.output)

# class FeeAllocationWithStudentViewSet(viewsets.ViewSet):
#     queryset = FeeAllocation.objects.all()

#     def list(self,request):
#         data = request.GET
#         student_id = data['student_id']
#         _class_id = data['_class_id']
        
#         output = []
#         ids = []
#         fci = []
#         final_list = []
#         obj = StudentPayment.objects.filter(fee_collection__student_id=student_id,fee_allocation___class_id=_class_id)
#         if obj:
#             for o in obj:
#                 fee_category_id = o.fee_allocation.fee_category.id
#                 if o.payment_status == 1:
#                     ids.append(fee_category_id)
                   
#                 else:
#                     if not fee_category_id in ids:
#                         if not fee_category_id in fci:
#                             fci.append(o.fee_allocation.fee_category.id)
#                             print(fci)
#                             temp ={
#                                     'fee_allocation_id':o.fee_allocation.id,
#                                     'fee_category':o.fee_allocation.fee_category.name,
#                                     'total_amount':o.fee_allocation.total_amount,
#                                     'paid_amount':o.paid_amount,
#                                     'receipt_number':o.fee_collection.receipt_number
#                                     }
#                             output.append(temp)
#             return Response(output)
#         else:
#             queryobj = FeeAllocation.objects.filter(_class_id=_class_id)
#             for q in queryobj:
#                 temp ={
#                 'fee_allocation_id':q.id,
#                 'fee_category':q.fee_category.name,
#                 'total_amount':q.total_amount,
#                 'paid_amount':0,
#                 }
#                 output.append(temp)
#             return Response(output)






# class FeeCollectionViewSet(viewsets.ViewSet):
#     queryset = FeeCollection.objects.all()

#     def create(self,request):
#         serializer = FeeCollectionSerializer(data=request.data)
#         if serializer.is_valid():
#             data = serializer.data
          
#             fc_obj,boo = FeeCollection.objects.get_or_create(student_id=data['student_id'],
#                                                           defaults={
#                                                             'receipt_number':data['receipt_number'],
#                                                               'mode_of_payment':data['mode_of_payment'],
#                                                               'remarks':data['remarks']
#                                                           }
#                                                             )
#             if not boo:
#                 obj = StudentPayment.objects.filter(fee_collection_id=fc_obj.id)
#                 for o in obj:
#                     for pd in data['payment_detail']:
#                         fee_allocation_id = pd['fee_allocation_id']
#                         if o.fee_allocation.id == fee_allocation_id:
#                             print(fee_allocation_id,o.fee_allocation.id)
#                             input_paid_amount = int(pd['paid_amount'])
#                             if input_paid_amount > 0:
#                                 if (o.fee_allocation.total_amount == input_paid_amount):
                                   
#                                     obj = StudentPayment.objects.create(fee_collection_id = fc_obj.id,
#                                                                     fee_allocation_id = fee_allocation_id,
#                                                                     paid_amount = pd['paid_amount'],
#                                                                     payment_status = 1
#                                                                 )

#                                 elif (o.fee_allocation.total_amount > input_paid_amount):
                                    
#                                     obj = StudentPayment.objects.create(fee_collection_id = fc_obj.id,
#                                                                     fee_allocation_id = fee_allocation_id,
#                                                                     paid_amount = pd['paid_amount'],
#                                                                     payment_status = 2
#                                                                 )
#                                 else:
#                                     obj = StudentPayment.objects.create(fee_collection_id = fc_obj.id,
#                                                                     fee_allocation_id = fee_allocation_id,
#                                                                     paid_amount = pd['paid_amount'],
#                                                                     payment_status = 3
#                                                                 )
#                 return Response('Updated data',status=status.HTTP_201_CREATED)

#             payment_detail = data['payment_detail']

#             for pd in payment_detail:
#                 fee_allocation = pd['fee_allocation_id']
#                 paid_amount = pd['paid_amount']
#                 paid_amount = int(paid_amount)
               
#                 fo = FeeAllocation.objects.get(id=fee_allocation)
#                 if fo.total_amount == paid_amount:
#                     obj,boo = StudentPayment.objects.get_or_create(fee_collection_id = fc_obj.id,
#                                                             fee_allocation_id = fee_allocation,
#                                                             defaults = {
#                                                                 'paid_amount':paid_amount,
#                                                                 'payment_status':1
#                                                             })

#                 elif fo.total_amount > paid_amount:
#                     obj,boo = StudentPayment.objects.get_or_create(fee_collection_id = fc_obj.id,
#                                                             fee_allocation_id = fee_allocation,
#                                                             defaults = {
#                                                                 'paid_amount':paid_amount,
#                                                                 'payment_status':2
#                                                             })
#                 else:
#                     obj,boo = StudentPayment.objects.get_or_create(fee_collection_id = fc_obj.id,
#                                                             fee_allocation_id = fee_allocation,
#                                                             defaults = {
#                                                                 'paid_amount':paid_amount,
#                                                                 'payment_status':3
#                                                             })
#                 if not boo:
#                     return Response("Fee_collection Should Be Unique",status=status.HTTP_400_BAD_REQUEST)
                                                       
           

#             return Response(data)
#         else:
#             raise serializers.ValidationError({
#                 'Details':[serializer.errors]
#             })

# class PaymentHistoryViewSet(viewsets.ViewSet):
#     queryset = StudentPayment.objects.all()

#     def list(self,request):
#         queryset = self.queryset
#         data = request.GET
#         student_id = data['student_id']
#         _class_id = data['class_id']
#         objects = StudentPayment.objects.filter(fee_collection__student_id=student_id,fee_allocation___class_id=_class_id)
        
#         output = []
#         for obj in objects:
#             paid_date = obj.date_created
#             if obj.paid_amount > 0:
#                 temp = {
#                     'name':obj.fee_collection.student.user.first_name + ' ' + obj.fee_collection.student.user.last_name,
#                     'fee_category':obj.fee_allocation.fee_category.name,
#                     'class':obj.fee_allocation._class.name,
#                     'receipt_number':obj.fee_collection.receipt_number,
#                     'paid_date':paid_date.strftime(('%m/%d/%Y %a,%H:%M %p')),
#                     'paid_amount':obj.paid_amount,
#                     'payment_status':obj.payment_status,
#                     'remarks':obj.fee_collection.remarks
#                 }
                
#                 output.append(temp)
#         return Response(output,status=status.HTTP_200_OK)




# class VoucherViewSet(viewsets.ViewSet):
#     queryset = StudentPayment.objects.all()

#     total_paid = 0
#     total_dues = 0
#     output = {}
#     remaining_to_pay = 0
#     remaining_dues = 0
#     total_balance = 0
#     total_remaining_dues = 0
#     balance = 0
  
#     def CalculatePaidAmmount(self,dues,paid):
#         if dues > paid:
#             self.remaining_dues = dues - paid
#             self.remaining_to_pay += dues - paid
            
#         elif dues == paid:
#             self.remaining_dues = dues - paid
           
            
#         else:
#             self.remaining_dues = 0
#             self.balance = paid-dues
#             self.total_balance += self.balance

#         self.total_paid += paid
#         self.total_dues += dues
     

       

#     def list(self,request):
#         self.output = {}
#         queryset = self.queryset
#         data = request.GET
#         student_id = data['student_id']
#         _class_id = data['class_id']
#         objects = StudentPayment.objects.filter(fee_collection__student_id=student_id,fee_allocation___class_id=_class_id)
#         templist = []
#         for obj in objects:
#             temp = {
#                 'id':obj.id,
#                 'fee_category':obj.fee_allocation.fee_category.name,
#                 'dues':obj.fee_allocation.total_amount,
#                 'date':obj.date_created.strftime(('%m/%d/%Y ,%I:%M:%S')),
#                 'paid':obj.paid_amount,
#             }

#             self.CalculatePaidAmmount(temp['dues'],temp['paid'])
#             temp['remaining_dues'] =self.remaining_dues
#             temp ['balance'] = self.balance
         
#             templist.append(temp)
#         if self.total_dues > self.total_paid:
#             self.total_remaining_dues += self.total_dues - self.total_paid
#         else:
#             self.total_remaining_dues = 0

#         self.output = {
#             'total_balance':self.total_balance,
#             'remaining_to_pay':self.remaining_to_pay,
#             'total_dues':self.total_dues,
#             'total_paid':self.total_paid,
#             'total_remaining_dues':self.total_remaining_dues,
#             'total_paid_in_words':num2words(self.total_paid)
#         }

#         self.output['payment_history'] = templist
        
#         newlist = sorted(self.output['payment_history'], key=itemgetter('date'),reverse=False)
#         self.output['payment_history'] = newlist
        
#         return Response(self.output,status=status.HTTP_200_OK) 

