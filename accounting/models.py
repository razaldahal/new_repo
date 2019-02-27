from django.db import models
from main.models import BaseModel
from academic.models import Class
from student.models import Student

class ExpenseCategory(BaseModel):
    name = models.CharField(max_length=120)
    description = models.CharField(max_length=120)

class DailyExpense(BaseModel):
    expense_type = models.ForeignKey(ExpenseCategory,on_delete=models.CASCADE)
    expense_detail = models.CharField(max_length=120)
    amount = models.IntegerField()
    expense_date = models.DateField()
    receipt_number = models.IntegerField(null=True,blank=True)

class FeeCategory(BaseModel):
    name = models.CharField(max_length=120)
    description = models.CharField(max_length=120)

class FeeAllocation(BaseModel):
    fee_category = models.ForeignKey(FeeCategory,on_delete=models.CASCADE)
    _class = models.ForeignKey(Class,on_delete=models.CASCADE)
    total_amount = models.IntegerField()
    def __str__(self):
        return (self.fee_category.name)


MODE_OF_PAYMENT = (
    (1,'CASH'),
    (2,'DEPOSIT'),
    (3,'CHEQUE'),
)
PAYMENT_STATUS = (
    (1,'Fully PAID'),
    (2,'PARTIALLY PAID'),
    (3,'PAID IN ADVANCE'),
    (4,'DUE')
)

PAYMENT_TYPE = (
    (1,'DUE'),
    (2,'PAID')
)

# class FeeCollection(BaseModel):
#     student = models.ForeignKey(Student,on_delete=models.CASCADE)
#     mode_of_payment = models.IntegerField(choices=MODE_OF_PAYMENT)
#     receipt_number = models.IntegerField()
#     remarks = models.TextField(max_length=500)
#     def __str__(self):
#         return (self.student.user.first_name)


class StudentPayment(BaseModel):
    student = models.ForeignKey(Student,on_delete=models.CASCADE)
    # receipt_number = models.IntegerField()
    remarks = models.TextField(max_length=500)
    #fee_collection = models.ForeignKey(FeeCollection,on_delete=models.CASCADE)
    fee_allocation = models.ForeignKey(FeeAllocation,on_delete=models.CASCADE)
    amount = models.IntegerField()
    payment_type = models.IntegerField(choices=PAYMENT_TYPE)
    payment_status = models.IntegerField(choices=PAYMENT_STATUS)


    def __str__(self):
        return (self.student.user.first_name + ' For ' + self.fee_allocation.fee_category.name)

# student_id = 1, fee_allocation = tutitoin , amount = 1000, payment_type = due
# student_id = 1, fee_allocation = tutitoin , amount = 900, payment_type = paid
# student_id = 1, fee_allocation = library , amount = 400, payment_type = due
# student_id = 1, fee_allocation = library , amount = 100, payment_type = due
# student_id = 1, fee_allocation = library , amount = 500, payment_type = paid


# Date	                Fee Category	    Dues	    Paid	Remaining Dues	Balance
# 02/15/2019 ,05:18:25	library	            -	        500	    100	            -100
# 02/14/2019 ,05:18:25	library	            100	        -	    600 	        -600
# 02/13/2019 ,05:18:25	library	            400	        -	    500	            -500
# 02/12/2019 ,05:18:25	tutitoin	        -       	900	    100	           -100
# 02/11/2019 ,05:18:25	tutitoin	        1000	    -	    0	            -1000