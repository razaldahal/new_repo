from django.urls import path,include
from rest_framework import routers

from . import views

router = routers.DefaultRouter()
router.register(r'expense-category',views.ExpenseCategoryViewSet)
router.register(r'daily-expense',views.DailyExpenseViewSet)
router.register(r'fee-category',views.FeeCategoryViewSet)
router.register(r'fee-allocation',views.FeeAllocationViewSet)
router.register(r'student_payment',views.FeeCollectionViewSet)
# router.register(r'allocation/student',views.FeeAllocationWithStudentViewSet)
# router.register(r'fee_allocation',views.FeeCollectionViewSet)
router.register(r'payment_history',views.PaymentHistoryViewSet)
# router.register(r'voucher',views.VoucherViewSet)


urlpatterns = [
	path('',include(router.urls)),

	]