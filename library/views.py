from django.shortcuts import render
from rest_framework import viewsets,status
from rest_framework.response import Response
from .models import *
from .serializers import *
from rest_framework import filters,generics
from django_filters.rest_framework import DjangoFilterBackend

# Create your views here.
class CategoryViewsets(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    
    def create(self,request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            data=serializer.data
            a,b = Category.objects.get_or_create(name=data['name'],section_code=data['section_code'])
            if not b:
                return Response({'Detail':'Category already added!'},status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response(data,status=status.HTTP_201_CREATED)
        else:
            return Response({'Detail':[serializer.errors]},status=status.HTTP_400_BAD_REQUEST)       

    def list(self,request):
        objects=self.queryset
        output=[]
        for obj in objects:
            temp={
                  'id':obj.id,
                  'name':obj.name,
                  'section_code':obj.section_code,
                  }
            output.append(temp)
        return Response(output)          


class BooksViewset(viewsets.ModelViewSet):
    queryset=Books.objects.all()
    serializer_class=BooksSerializer

    def create(self,request):
        serilaizer=self.get_serializer(data=request.data)
        if serilaizer.is_valid():
            data=serilaizer.data 
            a,b=Books.objects.get_or_create(purchase_date=data['purchase_date'],
            bill_no=data['bill_no'],
            isbn_no=data['isbn_no'],
            no=data['no'],
            title=data['title'],
            author=data['author'],
            edition=data['edition'],
            category=Category.objects.get(id=data['category']),
            publisher=data['publisher'],
            no_of_copies=data['no_of_copies'],
            shelf_no=data['shelf_no'],
            position=data['position'],
            book_cost=data['position'],
            book_condition=data['book_condition'])
            if not b:
                return Response('Book already exists',status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response(data,status=status.HTTP_201_CREATED)
        else:
            return Response({'Detail':[serilaizer.errors]},status=status.HTTP_400_BAD_REQUEST)

                   
    def list(self,request):
        objects=self.queryset
        output=[]
        for obj in objects:
            temp={'id':obj.id,
                'book_no':obj.no,
                  'book_isbn_no':obj.isbn_no,
                  'title': obj.title,
                  }
            output.append(temp)
        return Response(output)

class Issue_bookViewset(viewsets.ModelViewSet):
    queryset=Issue_book.objects.all()
    serializer_class=Issue_bookSerilaizer

    def create(self,request):
        serializer=self.get_serializer(data=request.data)
        if serializer.is_valid():
            data=serializer.data
            a,b=Issue_book.objects.get_or_create(user=User.objects.get(id=data['user']),user_type=data['user_type'],issue_date=data['issue_date'],due_date=data['due_date'],book=Books.objects.get(id=data['book']))
            if not b:
                return Response({'Detail':'Book already issued'},status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({'Success!':'Book issued successfully'},status=status.HTTP_201_CREATED)
        else:
            return Response({'Detail':[serializer.errors]},status=status.HTTP_400_BAD_REQUEST)

    def list(self,request):
        objects=self.queryset
        output=[]
        for obj in objects:
            temp={'book_no':obj.book.no,
                  'user':obj.user.first_name,
                  'user_type':obj.user_type,
                  'title':obj.book.title,
                  'issue_date':obj.issue_date,
                  'due_date':obj.due_date,
                  }
            output.append(temp)
        return Response(output)              
class Requset_bookViewsets(viewsets.ModelViewSet):
    queryset=Request_book.objects.all()
    serializer_class=Request_bookSerializer

    def list(self,request):
        objects=self.queryset
        for obj in objects:
            temp={'book_no':obj.book.no,
                  'user':obj.user.first_name,
                  'user_type':obj.user_type,
                  'title':obj.book.title,
                  'requested_date':obj.requested_date,
                  'accept/reject':obj.accept
                  }
            ouptput.append(temp)
        return Response(output)
    def create(self,request):
        serializer=self.get_serializer(data=request.data)
        if serializer.is_valid():
            data=serializer.data
            if request.user.is_active():
                a,b=Request_book.objects.get_or_create(user=User.objects.get(id=data['user']),user_type=data['user_type'],book=Books.objects.get(id=data['book']),requested_date=data['requested_date'])
                if not b:
                    return Response({'Detail':'Request already sent'},status=status.HTTP_400_BAD_REQUEST)
                else:
                    return Response({'Success!':'Request successfully created'},status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors)


class Book_returnViewsets(viewsets.ModelViewSet):
    serializer_class=Book_returnSerializer
    queryset=Book_return.objects.all()

    def create(self,request):
        serializer=self.get_serializer(data=request.data)
        if serializer.is_valid():
            data=serializer.data
            a,b=Book_return.objects.get_or_create(book=Issue_book.objects.get(book_id=data['book']),returned_date=data['returned_date'],fine_amount=data['fine_amount'],remarks=data['remarks'])
            if not b:
                return Response("Book returned instance already created")
            else:
                return Response('Book return successful')
        else:
            return Response(serilaizer.errors)
    def list(self,request):
        objects=self.queryset
        output=[]
        for obj in objects:
            temp={'user':obj.book.user.first_name,
                  'user_type':obj.book.user_type,
                  'returned_date':obj.returned_date,
                  'book_no':obj.book.book.no,
                  'author':obj.book.book.author,
                  'title':obj.book.book.title,
                  'fine_amount':obj.fine_amount,
                  'remarks':obj.remarks 
                }

            output.append(temp)
        return Response(output)                   
class SearchView(viewsets.GenericViewSet):
    queryset=Books.objects.all()
    serializer_class = BooksSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('title','purchase_date','bill_no','isbn_no',
    'no',
    'title',
    'author',
    'edition',
    'category__name',
    'publisher',
    'no_of_copies',
    'shelf_no',
    'position',
    'book_condition')
    def retrieve(self, request, pk=None):
        pass
    def list(self, request):
        pass
    
   


        # val=[]
        # ky=[]
        # res=[]
        # result=[]
        # for key in keys:
        #     a=qd.__getitem__(key)
        #     b=key
        #     val.append(a)
        #     ky.append(b)
        
        # for k in ky:
        #     for v in val:
        #         r=Books.objects.filter(k__icontains=v)
        #         s=r.count()
        #         for t in range [0:(s-1)]:
        #             book=r[t]
        #             res.append(book)
        #         result.append(res)
        # return Response(result)                               





            

         











