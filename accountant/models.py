from django.db import models
from main.models import BaseModel,User,Phone,Address
from student.models import Student
from teacher.models import Teacher
from Class.models import Class
from main.helpers.tuple import get_choice_string
payment_type_c=(
              (0,'MONTHLY'),
              (1,'TERMINAL'),
              (2,'ANNUAL'),
              (3,'ADMISSION'),
              (4,'OTHER_FEE')
              )
discount_type_c=(
            (0,'Scholarship'),
            (1,'Advanced_Fee_Submission'),
            (2,'Others'),
            (3,'ALL')
            )              
# Create your models here.
class Accountant(BaseModel):
    user= models.ForeignKey(User,on_delete=models.CASCADE)
    esp_id=models.SlugField(verbose_name='accountant_id',primary_key=True)
   




class PaymentType(BaseModel):
    name=models.IntegerField(choices=payment_type_c)
    _class=models.ForeignKey(Class,on_delete=models.CASCADE)
    rate=models.IntegerField()
    def get_name(self,obj):
        return get_choice_string(payment_type_c,obj.name)

    def __str__(self):
        return get_choice_string(payment_type_c,self.name)    

	
class Payments(BaseModel): 

    payment_type=models.ForeignKey(PaymentType,on_delete=models.CASCADE)
    paid_by=models.ForeignKey(User,on_delete=models.CASCADE)
    paid_amount=models.IntegerField()

    paid_to=models.ForeignKey(Accountant,on_delete=models.CASCADE)
    paid_method_c=(
                (0,'CASH'),
                (1,'CHEQUE'),
                )

    paid_for=models.ForeignKey(Student,on_delete=models.CASCADE)
    paid_method=models.IntegerField(choices=paid_method_c)
    cheque_no=models.CharField(max_length=100,default=None)
    date_of_transaction=models.DateField(auto_now_add=True)
    short_description=models.TextField()
    total_discount_amount=models.IntegerField(default=None)
    discount_type=models.IntegerField(choices=discount_type_c,null=True)    
    discount_description=models.TextField(blank=True)    
    fine_amount=models.IntegerField(default=None)
    fine_description=models.TextField(blank=True)
    time=models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together=('date_of_transaction','time')
class StudentAc(BaseModel):
    student=models.ForeignKey(Student,on_delete=models.CASCADE)
    payments=models.ForeignKey(Payments,on_delete=models.CASCADE)
    due_amount=models.IntegerField(default=None)
    credit_amount=models.IntegerField(default=None)
    balance=models.IntegerField(default=None)


class Fee_Category(BaseModel):
    name=models.CharField(max_length=50)
    description=models.TextField(blank=True)
class Fee_Allocation(BaseModel):
    fee_category=models.ForeignKey(Fee_Category,on_delete=models.CASCADE)
    _class=models.ForeignKey(Class,on_delete=models.CASCADE)
    amount=models.IntegerField()


class TeacherSalary(BaseModel):
    teacher=models.ForeignKey(Teacher,on_delete=models.CASCADE)
    year=models.IntegerField()
    month=models.IntegerField()
    salary=models.IntegerField()
    deduction=models.IntegerField()    