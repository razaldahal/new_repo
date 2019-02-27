from django.urls import path,include
from rest_framework import routers

from . import views

router = routers.DefaultRouter()
# router.register('test',views.TestStudentViewSet)
router.register('vendor',views.VendorViewSet)
router.register('product-category',views.ProductCategoryViewSet)
router.register('products',views.ProductsViewSet)


urlpatterns = [
	path('',include(router.urls))
]
