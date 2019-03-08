from rest_framework import viewsets,serializers,status
from rest_framework.views import APIView
from rest_framework.response import Response
from num2words import num2words
from datetime import datetime
from operator import itemgetter


from .serializers import *
from .models import *

class MethodSerializerView(object):
    method_serializer_classes = None

    def get_serializer_class(self):
        assert self.method_serializer_classes is not None, (
            'Expected view %s should contain method_serializer_classes '
            'to get right serializer class.' %
            (self.__class__.__name__, )
        )
        for methods, serializer_cls in self.method_serializer_classes.items():
            if self.request.method in methods:
                return serializer_cls

        raise exceptions.MethodNotAllowed(self.request.method)

class FacultyViewSet(MethodSerializerView,viewsets.ModelViewSet):
    queryset = FacultySalary.objects.all()

    method_serializer_classes = {
        ('POST'): FacultyPostSerializer,
        ('PUT'):FacultySalaryUpdateSerializer,
        ('GET'): FacultySalaryGetSerializer,
        }

    def update(self, request, pk):
        instance = self.get_object()
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            data = serializer.data
            instance.salary = data['salary']
            instance.save()
            return Response(data)

        else:
            raise serializers.ValidationError({'Detail':[serializer.errors]})


class FacultySalaryPaymentViewSet(MethodSerializerView,viewsets.ModelViewSet):
    queryset = FacultySalaryPayment.objects.all()
    # serializer_class = FacultySalaryPaymentSerializer

    method_serializer_classes = {
        ('POST'): FacultySalaryPaymentSerializer,
        # ('PUT'):FacultySalaryUpdateSerializer,
        # ('GET'): FacultySalaryPaymentGetSerializer,
        }
    def list(self,request):
        data = request.GET
        faculty_id = data['faculty_id']
        try:
            # obj = FacultySalaryPayment.objects.get(faculty__faculty_id=faculty_id)
            objects = self.queryset.filter(faculty_id=faculty_id)
            output = []
            total_paid = 0
            output_dict = {}
            output_dict['faculty_name'] = objects[0].faculty.user.first_name
            for obj in objects:
                temp = {
                    # 'faculty_name':obj.faculty.user.first_name ,
                    'amount':obj.amount,
                    'month':obj.month,
                    'date_paid':obj.date_created
                }
                total_paid += obj.amount
                output.append(temp)
            output_dict['paid_detail'] = output
            output_dict['total_paid'] = total_paid
            return Response(output_dict)
        except:
            return Response([])
        

class ExpenseCategoryViewSet(viewsets.ModelViewSet):
    queryset = ExpenseCategory.objects.all()
    serializer_class = ExpenseCategorySerializer

class DailyExpenseViewSet(viewsets.ModelViewSet):
    queryset = DailyExpense.objects.all()
    serializer_class = DailyExpenseSerializer

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
        output = []
        data = request.GET
        
        expense_category = data.get('expense_category', False)
        queryset = self.get_queryset()
        if expense_category and expense_category != '0':
            queryset = queryset.filter(expense_type_id=expense_category)

        if 'start_date' in data:
            queryset = queryset.filter(expense_date__range=[data['start_date'],data['end_date']])
        
        queryset = queryset.order_by('-expense_date')
        output = ExpenseGetSerializer(queryset, many=True).data
        return Response(output,status=status.HTTP_200_OK)


    def retrieve(self,request,pk):
        obj = self.get_object()
        output = ExpenseGetSerializer(obj).data
        output['expense_type'] = obj.expense_type.id
        return Response(output,status=status.HTTP_200_OK)

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


# class FeeAllocationViewSet(viewsets.ModelViewSet):
#     queryset = FeeAllocation.objects.all()

class FeeAllocationViewSet(viewsets.ModelViewSet):
    queryset = FeeAllocation.objects.all()
    serializer_class = FeeAllocationSerializer

    def get_serializer(self, *args, **kwargs):
        serializer_class = self.get_serializer_class()
        if self.request.method == 'GET':
            serializer_class = FeeAllocationGetSerializer
        return serializer_class(*args, **kwargs)

    def create(self,request):
        serializer = FeeAllocationSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.data
            fee_for = data['fee_for']

            if fee_for == 1:
                class_obj = Class.objects.all()
                
                for c_obj in class_obj:
                    class_id = c_obj.id
                    obj,created = FeeAllocation.objects.update_or_create(
                        fee_category_id=data['fee_category'],
                        _class_id =class_id,
                        defaults = {'total_amount':data['total_amount']})

                return Response(data,status=status.HTTP_201_CREATED)

            if fee_for==2:
                obj,created = FeeAllocation.objects.update_or_create(
                    fee_category_id=data['fee_category'],
                    _class_id = data['_class'],
                    defaults = {'total_amount':data['total_amount']})

                if created:
                    return Response(data,status=status.HTTP_201_CREATED)
           
        else:
            raise serializers.ValidationError({
                'Detail':[serializer.errors]
            })



    def update(self,request,pk):
        obj = self.get_object()
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
        queryset = self.get_queryset()
        data = request.GET
        if '_class_id' in data:
            queryset = queryset.filter(_class_id=data['_class_id'])

        data = self.get_serializer(queryset, many=True).data
        return Response(data)




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
                            remarks = data.get('remarks', False),
                            amount = data['amount'],
                            payment_status = 2,
                            payment_type = int(data['payment_type'])
                            )

            elif total_amount == paid_amount:
                obj = StudentPayment.objects.create(
                            fee_allocation_id = data['fee_allocation_id'],
                            student_id = data['student_id'],
                            remarks = data.get('remarks',False),
                            amount = data['amount'],
                            payment_status = 1,
                            payment_type = int(data['payment_type'])
                            )

            else:
                obj = StudentPayment.objects.create(
                            fee_allocation_id = data['fee_allocation_id'],
                            student_id = data['student_id'],
                            remarks = data.get('remarks',False),
                            amount = data['amount'],
                            payment_status = 3,
                            payment_type = int(data['payment_type'])
                        )
            
            return Response(data ,status=status.HTTP_201_CREATED)
        else:
            raise serializers.ValidationError({
                'Detail':[serializer.errors]
            })


class PaymentHistoryViewSet(viewsets.ModelViewSet):
    queryset = StudentPayment.objects.all()
    serializer_class = StudentPaymentSerializer
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
        queryset = self.get_queryset()
        data = request.GET
        student_id = data['student_id']
        objects = StudentPayment.objects.filter(student_id=student_id).order_by('date_created')
        histories = []

        '''
        Date particulars debit  credit balance
        '''

        '''
        Date        particulars         amount     pending dues.    Balance    remarks
        2019-3-1    Admission Fee       5000       5000          -5000       Need to pay admission fee
        2019-3-2    Admission Fee paid. 4500       500           -500        Paid admission fee partially
        2019-3-3    Admission Fee paid. 1000       0             500         Paid admission
        '''

        current_due = 0
        current_balance = 0
        for obj in objects:
            

            ## if due
            if obj.payment_type == 1:
                current_due += obj.amount
                current_balance -= obj.amount

            else:
                current_due -= obj.amount
                current_balance += obj.amount



            tmp = {
                'date': datetime.strftime(obj.date_created, '%Y-%m-%d %I:%M %p'),
                'category': obj.fee_allocation.fee_category.name,
                'particulars': obj.remarks,
                'amount': obj.amount,
                'pending_dues': current_due,
                'balance': current_balance,
                'payment_type': obj.payment_type
            } 
            histories.append(tmp)           
        
        histories = histories[::-1]
        return Response(histories)
        # for obj in objects:
        #     temp = {
        #         'paid_date':obj.date_created.strftime(('%m/%d/%Y %a,%H:%M %p')),
        #         'fee_category':obj.fee_allocation.fee_category.name,
        #         'fee_category_id':obj.fee_allocation.fee_category.id,
        #         'dues':obj.fee_allocation.total_amount,
        #         'paid_amount':obj.amount,
        #         'payment_status':obj.payment_status,
        #         'payment_type':obj.payment_type,
        #         }
        #     self.PaymentStateMentDetail(temp)
        #     temp['remaining_dues'] = self.remaining_dues
        #     temp['total_balance'] = self.total_balance
        #     self.output.append(temp)
            
        # # payment_history['payment_history'] = output
       
        # # newlist = sorted(output, key=itemgetter('paid_date'),reverse=True)
        # return Response(self.output)
