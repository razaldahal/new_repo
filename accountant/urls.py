from django.urls import path,include
from rest_framework import routers

from accountant import views

router = routers.DefaultRouter()
router.register(r'accountant',views.AccountantViewset)
router.register(r'paymenttype',views.PaymentTypeViewSet)
router.register(r'payments',views.PaymentsViewSet)
router.register(r'studentac',views.StudentAcViewSet)
router.register(r'feecategory',views.Fee_CategoryViewSet)
router.register(r'feeallocation',views.Fee_AllocationViewSet)
router.register(r'teachersalary',views.TeacherSalaryViewset)
urlpatterns = [
	path('',include(router.urls)),

	]