from django.db import models
from main.models import BaseModel,User,USER_TYPE
# Create your models here.


class Category(BaseModel):
    name=models.CharField(max_length=30)
    section_code=models.SlugField()

    def __str__(self):
        return self.name


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
    book_condition_c=(
    (1,'AS NEW'),
    (2,'FINE'),
    (3,'VERY GOOD'),
    (4,'GOOD'),
    (5,'FAIR'),
    (6,'POOR'),
    (7,'LOST'),
    (8,'MISSING')
    )
    book_condition=models.IntegerField(choices=book_condition_c)
    def __str__(self):
        return self.title+" "+self.isbn_no


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
    accept=models.NullBooleanField()
class Book_return(BaseModel):
    book=models.ForeignKey(Issue_book,on_delete=models.CASCADE)
    returned_date=models.DateField()
    fine_amount=models.IntegerField()
    remarks=models.TextField()