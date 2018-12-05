from django.db import models
from main.models import BaseModel,User,Phone,Address
from student.models import Student
payment_type_c=(
              (0,'MONTHLY'),
              (1,'TERMINAL'),
              (2,'ANNUAL')
              )
# Create your models here.
class Accountant(BaseModel):
    user= models.ForeignKey(User,on_delete=models.CASCADE)
    esp_id=models.SlugField(verbose_name='accountant_id',primary_key=True)
   

	
	
	
class Payments(BaseModel):                
    payment_type=models.IntegerField(choices=payment_type_c)
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
    date_time_of_transaction=models.DateTimeField(auto_now_add=True,unique=True)
    short_description=models.TextField()

class Payment_posting_reference(BaseModel):
    payment_details = models.ForeignKey(Payments,on_delete=models.CASCADE)
    balance = models.IntegerField(help_text="Negative for dues,0 for all accounts cleared, Positive if payeee is to receive instead")

class Ledger(BaseModel):
    payment_posting_reference = models.ForeignKey(Payment_posting_reference,on_delete=models.CASCADE)
    description = models.TextField()

class Studentpayments(BaseModel):
    student = models.ForeignKey(Student,on_delete=models.CASCADE)
    payments = models.ForeignKey(Payments,on_delete=models.CASCADE)
    ledger = models.ForeignKey(Ledger,on_delete=models.CASCADE)

class Fees_due(BaseModel):
    student=models.ForeignKey(Student,on_delete=models.CASCADE)
    fee_type=models.IntegerField(choices=payment_type_c)
    ac_start_date=models.DateField()
    rate=models.IntegerField()
    date=models.DateField()