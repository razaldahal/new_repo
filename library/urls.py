from django.urls import path,include
from rest_framework import routers

from library import views

router = routers.DefaultRouter()
router.register(r'category',views.CategoryViewsets)
router.register(r'books',views.BooksViewset)
router.register(r'issue',views.Issue_bookViewset)
router.register(r'return',views.Book_returnViewsets)
router.register(r'search',views.SearchViewset)
urlpatterns = [
	path('',include(router.urls)),

]