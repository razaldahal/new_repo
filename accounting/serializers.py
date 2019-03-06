from rest_framework import serializers
from .models import *
from rest_framework.validators import UniqueTogetherValidator
from academic.serializers import FacultySerializer

class FacultySalaryGetSerializer(serializers.ModelSerializer):
    faculty = FacultySerializer()
    class Meta:
        model = FacultySalary
        fields = ('__all__')

class FacultySerializer(serializers.ModelSerializer):
    faculty_id = serializers.IntegerField()
    
    class Meta:
        model = FacultySalary
        fields = (
            'id','faculty_id','salary','remarks',
            )
        validators = [
            UniqueTogetherValidator(
                queryset=FacultySalary.objects.all(),
                fields=('faculty_id',)
            )
        ]
class FacultySalaryUpdateSerializer(serializers.ModelSerializer):
    faculty_id = serializers.IntegerField()
    class Meta:
        model = FacultySalary
        fields = ('faculty_id','salary')
    

    
class ExpenseCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ExpenseCategory
        fields = ('id','name','description')

class DailyExpenseSerializer(serializers.ModelSerializer):
    expense_type = serializers.IntegerField()
    class Meta:
        model = DailyExpense
        fields = ('id','expense_type','expense_detail','amount','expense_date','receipt_number')

class FeeCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = FeeCategory
        fields = ('id','name','description')

class FeeAllocationSerializer(serializers.Serializer):
    fee_for = serializers.IntegerField()
    _class = serializers.IntegerField(required=False)
    fee_category = serializers.IntegerField()
    total_amount = serializers.IntegerField()



class FeeAllocationGetSerializer(serializers.ModelSerializer):
    course = serializers.CharField(source='_class.course.name')
    _class = serializers.CharField(source='_class.name')
    fee_category = serializers.CharField(source='fee_category.name')
    total_amount = serializers.FloatField()

    class Meta:
        model = FeeAllocation
        fields = ('id', 'course', '_class', 'fee_category', 'total_amount', )

class FeeAllocationUpdateSerializer(serializers.Serializer):
    total_amount = serializers.IntegerField()

class FeeCollectionSerializer(serializers.Serializer):
    payment_detail = serializers.ListField()
    student_id = serializers.IntegerField()
    mode_of_payment = serializers.IntegerField(required=False,default=1)
    receipt_number = serializers.IntegerField(required=False)
    remarks = serializers.CharField(required=False)


class StudentPaymentSerializer(serializers.Serializer):
    fee_allocation_id = serializers.IntegerField()
    amount = serializers.IntegerField()
    student_id = serializers.IntegerField()
    remarks = serializers.CharField(required=False)

