from django.db import models
from main.models import BaseModel,User,USER_TYPE
# Create your models here.


class Category(BaseModel):
    name=models.CharField(max_length=30)
    section_code=models.SlugField()

class Books(BaseModel):
    purchase_date=models.DateField()
    bill_no=models.CharField(max_length=20)
    isbn_no=models.SlugField()
    no=models.CharField(max_length=20)
    title=models.CharField(max_length=30)
    author=models.CharField(max_length=30)
    edition=models.CharField(max_length=20)
    category=models.ForeignKey(Category,on_delete=models.CASCADE)
    publisher=models.CharField(max_length=30)
    no_of_copies=models.IntegerField()
    shelf_no=models.CharField(max_length=20)
    position=models.CharField(max_length=20)
    book_cost=models.IntegerField()
    book_condition=(
    ('As_new','AS NEW'),
    ('fine','FINE'),
    ('verygood','VERY GOOD'),
    ('good','GOOD'),
    ('fair','FAIR'),
    ('poor','POOR'),
    ('lost','LOST'),
    ('missing','MISSING')
    )
    book_condition=models.CharField(max_length=15,choices=book_condition)

class Issue_book(BaseModel):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    user_type=models.CharField(max_length=15,choices=USER_TYPE)
    book=models.ForeignKey(Books,on_delete=models.CASCADE)
    issue_date=models.DateField()
    due_date=models.DateField() 
class Request_book(BaseModel):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    user_type=models.CharField(max_length=15,choices=USER_TYPE)
    book=models.ForeignKey(Books,on_delete=models.CASCADE)
    request_date=models.DateField()
    status=models.CharField(max_length=10)
    accept=models.BooleanField(null=True)
class Book_return(BaseModel):
    book=models.ForeignKey(Issue_book,on_delete=models.CASCADE)
    returned_date=models.DateField()
    fine_amount=models.IntegerField()
    remarks=models.TextField()